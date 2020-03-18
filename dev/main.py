from python_libs import config
from python_libs.secret_manager import Secret_Manager
from python_libs.loggers import logger,Price_Logger
from python_libs.ig_client import IG_Client
from python_libs.market import Market_Streamer
from python_libs.data_processor import Data_Processor


logger.info('IDENTIFIER: %s, IG_BASE_URL: %s' %(config.IDENTIFIER,config.IG_BASE_URL))

sm=Secret_Manager()
sm.get_secret()

ig=IG_Client(config.IG_BASE_URL,config.IDENTIFIER,sm.secret['ig_password'],sm.secret['ig_api_key'])
ig.login()

session_info=ig.get_session_info()
logger.info(session_info)

market_streamer=Market_Streamer(session_info["lightstreamerEndpoint"],config.IDENTIFIER,ig.CST,ig.X_SECURITY_TOKEN)



from python_libs.bidder import Bidder
from python_libs.dealer import Dealer


bidders=[Bidder(i) for i in range(6)]

bidders[0].set_behaviour(order_type='buy',stop=10,limit=10)
bidders[1].set_behaviour(order_type='buy',stop=20,limit=20)
bidders[2].set_behaviour(order_type='buy',stop=50,limit=50)
bidders[3].set_behaviour(order_type='sell',stop=10,limit=10)
bidders[4].set_behaviour(order_type='sell',stop=20,limit=20)
bidders[5].set_behaviour(order_type='sell',stop=50,limit=50)


dealer=Dealer()

def event_handler(item):
    timestamp=item["timestamp"]
    bid=float(item["values"]["BID"])
    offer=float(item["values"]["OFFER"])
    orders=[bidder.order() for bidder in bidders]
    dealer.process_orders(orders,bid,offer,timestamp)
    price_logger.log(item)
    pass

market_streamer.subscribe(config.EPIC,event_handler)
price_logger=Price_Logger(config.EPIC)

dp=Data_Processor()
dp.start()


while(True):
    pass