import threading, os, time

from pathlib import Path
from datetime import datetime as dt
import math
import io


import pandas as pd
import numpy as np

import sagemaker.amazon.common as smac
import boto3

from python_libs import config
from python_libs.loggers import logger

cwd=Path(__file__).parent.parent

cwd.joinpath('data').mkdir(parents=True, exist_ok=True)

data_dir=cwd.joinpath('data')
log_dir=cwd.joinpath('logs')

import logging

def merge_log_files(prefix):
    files_to_be_merged=log_dir.joinpath(prefix+'*')
    destination_file=data_dir.joinpath(prefix+'.csv')
    merge_command='cat %s > %s' % (files_to_be_merged,destination_file)
    os.system(merge_command)
    logger.info('%s* merged into %s' %(files_to_be_merged,destination_file))

def process_data(deal_data_path,price_data_path):
    logger.info('Starting data processing')

    logger.info('Getting deals from CSV')
    deals=pd.read_csv(deal_data_path,
        header=None,
        names=["timestamp","deal_type","order_type","stop","limit","price","stop_price","limit_price","loss_or_profit"],
        dtype={
            "timestamp":str
        }
    )

    query='order_type=="buy" & stop==10'
    logger.info('Getting qualified deals - %s' % query)
    qualified_deals=deals.query(query)

    logger.info('Getting price from CSV')
    price=pd.read_csv(price_data_path,
        header=None,
        names=["datetime","timestamp","MID_OPEN","BID","OFFER","CHANGE","CHANGE_PCT","HIGH","LOW"],
        dtype={
            "timestamp":str,
            "datetime":str
        }
    )

    logger.info('Joining deals with price')
    deals_with_price=pd.merge(qualified_deals, price,how="inner",on="timestamp",sort=True)

    # Calculating MID price, the average of BID and OFFER
    deals_with_price['MID']=(deals_with_price['BID']+deals_with_price['OFFER'])/2

    _format='%y-%m-%d %H:%M:%S'

    def datetime_to_int(x):
        return int(dt.strptime(x,_format).timestamp())

    # Parsing the datetime string to get the timestamp(seconds) to match the price
    # Note that this timestamp is different from the timestamp of the message
    deals_with_price['datetime_int']=deals_with_price['datetime'].apply(datetime_to_int)

    mean_price_each_second=deals_with_price[['datetime','BID','OFFER']].groupby('datetime').mean().reset_index()
    mean_price_each_second['datetime_int']=mean_price_each_second['datetime'].apply(datetime_to_int)
    mean_price_each_second['MID']=(mean_price_each_second['BID']+mean_price_each_second['OFFER'])/2

    df=pd.DataFrame()
    historical_data_points=600
    for i,row in deals_with_price.iterrows():
        values=np.full(historical_data_points,np.nan)
        _timestamp=row['datetime_int']
        prices=mean_price_each_second[['datetime_int','MID']].query('datetime_int<%s' % _timestamp).tail(historical_data_points)['MID']
        values[0:len(prices)]=prices.values
        value_series=pd.Series(values)
        df.insert(loc=i,column=str(row['timestamp']),value=values)

    all_data_absolute=deals_with_price[['timestamp','BID','OFFER','MID_OPEN','HIGH','LOW']].merge(df.transpose(),left_on='timestamp',right_index=True)

    all_data_absolute.drop('timestamp',axis=1,inplace=True)
    all_data_absolute.fillna(method='backfill',inplace=True)
    all_data_absolute.fillna(method='pad',inplace=True)

    mid=(all_data_absolute['BID']+all_data_absolute['OFFER'])/2

    all_data=all_data_absolute.subtract(mid,axis='index')

    labels=deals_with_price['deal_type'].apply(lambda x:1 if x=='limit' else 0)

    count=len(all_data)

    training=math.floor(0.7*count)
    validation=math.floor(0.15*count)
    test=math.floor(0.15*count)
    
    training_data_set=all_data[0:training]
    training_labels=labels[0:training]

    test_data_set=all_data[(training+1):(training+test)]
    test_labels=labels[(training+1):(training+test)]

    validation_data_set=all_data[(training+test+1):]
    validation_labels=labels[(training+test+1):]

    training_data_set.to_csv(data_dir.joinpath('training_data.csv'),header=None,index=False)
    test_data_set.to_csv(data_dir.joinpath('test_data.csv'),header=None,index=False)
    validation_data_set.to_csv(data_dir.joinpath('validation_data.csv'),header=None,index=False)

    training_data_np=training_data_set.to_numpy().astype('float32')
    training_labels_np=training_labels.to_numpy().astype('float32')

    test_data_np=test_data_set.to_numpy().astype('float32')
    test_labels_np=test_labels.to_numpy().astype('float32')

    validation_data_np=validation_data_set.to_numpy().astype('float32')
    validation_labels_np=validation_labels.to_numpy().astype('float32')

    session=boto3.Session()

    buf = io.BytesIO()
    smac.write_numpy_to_dense_tensor(buf, training_data_np, training_labels_np)
    buf.seek(0)
    session.resource('s3').Bucket(config.BUCKET).Object('training_data.io').upload_fileobj(buf)

    buf = io.BytesIO()
    smac.write_numpy_to_dense_tensor(buf, test_data_np, test_labels_np)
    buf.seek(0)
    session.resource('s3').Bucket(config.BUCKET).Object('test_data.io').upload_fileobj(buf)

    buf = io.BytesIO()
    smac.write_numpy_to_dense_tensor(buf, validation_data_np, validation_labels_np)
    buf.seek(0)
    session.resource('s3').Bucket(config.BUCKET).Object('validation_data.io').upload_fileobj(buf)

    evaluation_data=all_data.copy()
    evaluation_data['profit']=labels

    evaluation_data.to_csv(data_dir.joinpath('evaluation_data.csv'),header=None,index=False)

    s3 = boto3.client('s3')
    with open(data_dir.joinpath('evaluation_data.csv'), "rb") as f:
        s3.upload_fileobj(f, config.BUCKET,'evaluation_data.csv')

    pass
    

class Data_Processor:
    def __init__(self):
        self.deal_prefix='deals-%s.log' % config.EPIC # Deal log file has rotated
        self.price_prefix='price-%s.log' % config.EPIC # Price log file does not have to be rotated
        self.deal_data_path=data_dir.joinpath(self.deal_prefix+'.csv')
        self.price_data_path=data_dir.joinpath(self.price_prefix+'.csv')
        self.thread= threading.Thread(target=self.log_watcher)

    def start(self):
        self.thread.start()
        return self.thread

    def log_watcher(self):
        while(1):
            for f_name in os.listdir(log_dir):
                if f_name.startswith(self.deal_prefix+'.'): 
                    logger.info('Found file %s' % f_name)
                    merge_log_files(self.deal_prefix)
                    merge_log_files(self.price_prefix)
                    os.remove(log_dir.joinpath(f_name))
                    process_data(self.deal_data_path,self.price_data_path)
                    break
                else:
                    logger.debug('%s does not match pattern %s*' % (f_name,self.deal_prefix))
            time.sleep(5)