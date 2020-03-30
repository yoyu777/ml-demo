# to be used in Glue jobs only
import sys
from awsglue.utils import getResolvedOptions
args = getResolvedOptions(sys.argv,['JOB_NAME','S3_BUCKET','deal_data_key','price_data_key'])

from datetime import datetime as dt
import math
import io
import logging,os


import pandas as pd
import numpy as np

import sagemaker.amazon.common as smac
import boto3
from s3fs.core import S3FileSystem

s3fs = S3FileSystem(anon=False)
session=boto3.Session()

S3_BUCKET=args['S3_BUCKET']
deal_data_path='s3://%s/staging/%s' % (S3_BUCKET,args['deal_data_key'])
price_data_path='s3://%s/staging/%s' % (S3_BUCKET,args['price_data_key'])

def initialise_logger():
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "WARN"),
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M')

    logger=logging.getLogger('data-processor')
    return logger

def get_deal_data(deal_data_path):
    logger.warn('Getting deals from CSV')

    deals=pd.read_csv(s3fs.open(deal_data_path),
        header=None,
        names=["timestamp","loss_or_profit","type","stop","limit","price","stop_price","limit_price"],
        dtype={
            "timestamp":str
        }
    )

    query='type=="buy" & stop==10'
    logger.warn('Getting qualified deals - %s' % query)
    qualified_deals=deals.query(query)
    return qualified_deals

def get_price_data(price_data_path):
    logger.warn('Getting price from CSV')
    price=pd.read_csv(s3fs.open(price_data_path),
        header=None,
        names=["timestamp","BID","OFFER","MID_OPEN","CHANGE","CHANGE_PCT","HIGH","LOW","UPDATE_TIME","MARKET_STATE","MARKET_DELAY"],
        dtype={
            "timestamp":str,
            "datetime":str
        }
    )
    return price

def join_deals_with_price(qualified_deals,price):
    logger.warn('Joining deals with price')
    deals_with_price=pd.merge(qualified_deals, price,how="inner",on="timestamp",sort=True)

    # Calculating MID price, the average of BID and OFFER
    deals_with_price['MID']=(deals_with_price['BID']+deals_with_price['OFFER'])/2

    return deals_with_price

def calculate_mean_price_each_second(price):
    logger.warn('Calculating mean price for each second')
    price['timestamp_second']=round(price['timestamp'].astype(float)/1000)
    mean_price_each_second=price[['timestamp_second','BID','OFFER']].groupby('timestamp_second').mean().reset_index()
    mean_price_each_second['MID']=(mean_price_each_second['BID']+mean_price_each_second['OFFER'])/2
    return mean_price_each_second

def get_historical_price(deals_with_price,mean_price_each_second):
    logger.warn('Getting historical price for each deal')

    deals_with_price['timestamp_second']=round(deals_with_price['timestamp'].astype(float)/1000)

    df=pd.DataFrame()
    historical_data_points=600
    for i,row in deals_with_price.iterrows():
        values=np.full(historical_data_points,np.nan)
        _timestamp=row['timestamp_second']
        prices=mean_price_each_second[['timestamp_second','MID']].query('timestamp_second<%s' % _timestamp).tail(historical_data_points)['MID']
        values[0:len(prices)]=prices.values
        value_series=pd.Series(values)
        df.insert(loc=i,column=str(row['timestamp']),value=values)

    all_data_absolute=deals_with_price[['timestamp','BID','OFFER','MID_OPEN','HIGH','LOW']].merge(df.transpose(),left_on='timestamp',right_index=True)
    all_data_absolute.drop('timestamp',axis=1,inplace=True)

    logger.warn('Filling missing data')

    all_data_absolute.fillna(method='backfill',inplace=True)
    all_data_absolute.fillna(method='pad',inplace=True)

    return all_data_absolute

def calculate_relative_price(all_data_absolute):
    logger.warn('Calculating the price relative to MID for each deal')
    mid=(all_data_absolute['BID']+all_data_absolute['OFFER'])/2
    all_data=all_data_absolute.subtract(mid,axis='index')
    return all_data

def get_labels(deals_with_price):
    logger.warn('Getting labels for each deal')
    labels=deals_with_price['loss_or_profit'].apply(lambda x:1 if x=='profit' else 0)
    return labels

def create_datasets(all_data,labels):
    logger.warn('Creating datasets')
    count=len(all_data)

    training=math.floor(0.6*count)
    validation=math.floor(0.2*count)
    test=math.floor(0.2*count)

    datasets={
        'training':{},
        'validation':{},
        'test':{}
    }

    datasets['training']['data']=all_data[0:training]
    datasets['training']['labels']=labels[0:training]

    logger.warn('Training dataset created')

    datasets['validation']['data']=all_data[(training+1):(training+validation)]
    datasets['validation']['labels']=labels[(training+1):(training+validation)]

    logger.warn('Validation dataset created')

    datasets['test']['data']=all_data[(training+validation+1):]
    datasets['test']['labels']=labels[(training+validation+1):]

    logger.warn('Test dataset created')

    logger.warn("training data length: %s, training label length: %s" %(len(datasets['training']['data']),len(datasets['training']['labels'])))
    logger.warn("validation data length: %s, validation label length: %s" %(len(datasets['validation']['data']),len(datasets['validation']['labels'])))
    logger.warn("test data length: %s, test label length: %s" %(len(datasets['test']['data']),len(datasets['test']['labels'])))

    return datasets

def save_dataset(dataset,key):
    data_np=dataset['data'].to_numpy().astype('float32')
    labels_np=dataset['labels'].to_numpy().astype('float32')

    buf = io.BytesIO()
    smac.write_numpy_to_dense_tensor(buf, data_np, labels_np)
    buf.seek(0)
    session.resource('s3').Bucket(S3_BUCKET).Object('transformed/%s_data.io' % key).upload_fileobj(buf)
    logger.warn('%s dataset saved to S3' % key)

def save_datasets(datasets):
    logger.warn('Saving datasets')
    for key in datasets:
        save_dataset(datasets[key],key)

def save_all_data_as_csv(all_data):
    logger.warn('Saving all data as CSV for verification')
    csv_data=all_data.copy()
    csv_data['profit']=labels

    csv_data.to_csv('all_data.csv',header=None,index=False)

    s3 = session.client('s3')
    with open('all_data.csv', "rb") as f:
        s3.upload_fileobj(f, S3_BUCKET,'transformed/all_data.csv')
        logger.warn('CSV saved to S3')

logger=initialise_logger()

logger.warn('Starting data processing')

qualified_deals=get_deal_data(deal_data_path)

price=get_price_data(price_data_path)

deals_with_price=join_deals_with_price(qualified_deals,price)

mean_price_each_second=calculate_mean_price_each_second(price)

all_data_absolute=get_historical_price(deals_with_price,mean_price_each_second)

all_data=calculate_relative_price(all_data_absolute)

labels=get_labels(deals_with_price)

datasets=create_datasets(all_data,labels)

save_datasets(datasets)

save_all_data_as_csv(all_data)
