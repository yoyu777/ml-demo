from pathlib import Path

import pandas as pd

from python_libs import config
from python_libs.loggers import logger
from python_libs.bidder import Bidder
from python_libs.dealer import Dealer

EPIC="CS.D.GBPUSD.CFD.IP"


bidders=[Bidder(i) for i in range(6)]

bidders[0].set_behaviour(order_type='buy',stop=10,limit=10)
bidders[1].set_behaviour(order_type='buy',stop=20,limit=20)
bidders[2].set_behaviour(order_type='buy',stop=50,limit=50)
bidders[3].set_behaviour(order_type='sell',stop=10,limit=10)
bidders[4].set_behaviour(order_type='sell',stop=20,limit=20)
bidders[5].set_behaviour(order_type='sell',stop=50,limit=50)

dealer=Dealer()

data_path=Path(__file__).parent.parent.joinpath('data')

def event_handler(item):
    timestamp=item["timestamp"]
    bid=float(item["values"]["BID"])
    offer=float(item["values"]["OFFER"])
    orders=[bidder.order() for bidder in bidders]
    dealer.process_orders(orders,bid,offer,timestamp)
    price_logger.log(item)
    pass

price_df=pd.read_csv(data_path.joinpath('price.csv'),
    header=None,
    names=["datetime","timestamp","MID_OPEN","BID","OFFER","CHANGE","CHANGE_PCT","HIGH","LOW"],
    dtype={
        "timestamp":str,
        "datetime":str
    })

for i,row in price_df.iterrows():
    timestamp=row['timestamp']
    bid=row["BID"]
    offer=row["OFFER"]
    orders=[bidder.order() for bidder in bidders]
    dealer.process_orders(orders,bid,offer,timestamp)
    pass