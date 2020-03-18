import logging,os,json
from pathlib import Path
from datetime import datetime as dt

from logging.handlers import TimedRotatingFileHandler,RotatingFileHandler


logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"),
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M')

cwd=Path(__file__).parent.parent

cwd.joinpath('logs').mkdir(parents=True, exist_ok=True)

log_file=RotatingFileHandler(cwd.joinpath('logs/ml-lab-local.log'), 
                                                    mode='w',
                                                    maxBytes= 1*1000*1000,
                                                    backupCount=10)
logger=logging.getLogger(__file__)
logger.addHandler(log_file)

logger.info('loggers initialised')


class Price_Logger:
    def __init__(self,epic):
        cwd=Path(__file__).parent.parent

        price_log_handler=RotatingFileHandler(cwd.joinpath('logs/price-%s.log' % epic),
            maxBytes= 1*1000*1000,
            backupCount=10
        )

        self.price_logger=logging.getLogger('price-'+epic)

        self.price_logger.addHandler(price_log_handler)
        self.price_logger.setLevel(logging.INFO)
        self.price_logger.propagate=False

        logger.info('price logger initialised')

    def log(self,item):
        if ('timestamp' in item) and ('values' in item) and len(item['values'])>0:
            value_headers=["MID_OPEN","BID","OFFER","CHANGE","CHANGE_PCT","HIGH","LOW"]
            values=[item['values'][header] for header in value_headers]
            date=dt.today().strftime("%y-%m-%d")
            data=[date+' '+item['values']['UPDATE_TIME'],item['timestamp']]+values
            self.price_logger.info(
                ','.join(data)
            )
            return

class Deal_Logger:
    def __init__(self,epic):
        cwd=Path(__file__).parent.parent

        deal_log_handler=RotatingFileHandler(cwd.joinpath('logs/deals-%s.log' % epic),
            # maxBytes= 1*1000*1000,
            maxBytes=1*1000*1000,
            backupCount=10
        )

        self.deal_logger=logging.getLogger('deals-'+epic)

        self.deal_logger.addHandler(deal_log_handler)
        self.deal_logger.setLevel(logging.INFO)
        self.deal_logger.propagate=False

        logger.info('deal logger initialised')

    def log(self,row):
        if len(row)>0:
            headers=["timestamp","deal_type","order_type","stop","limit","price","stop_price","limit_price","loss_or_profit"]
            deal_data=[json.dumps(row[header]) for header in headers]
            self.deal_logger.info(','.join(deal_data))
        return
