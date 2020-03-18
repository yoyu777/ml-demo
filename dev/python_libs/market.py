from python_libs.lightstreamer_client import LightstreamerClient, LightstreamerSubscription
from python_libs.loggers import logger
from python_libs import config
from concurrent.futures import ThreadPoolExecutor


class Market_Streamer(object):
    def __init__(self,lightstreamer_endpoint,identifier,CST,X_SECURITY_TOKEN):
        self.ls_client=LightstreamerClient(
            lightstreamer_url=lightstreamer_endpoint,
            lightstreamer_username=identifier,
            lightstreamer_password="CST-%s|XST-%s" %(CST,X_SECURITY_TOKEN)
        )

        try:
            self.ls_client.connect()
        except Exception as e:
            logger.error(e)
            logger.error("Unable to connect to Lightstreamer Server")

    def subscribe(self,epic,event_handler):
        self.epic=epic

        self.subscription = LightstreamerSubscription(
            mode="MERGE",
            items=['MARKET:%s' % epic],
            fields=["UPDATE_TIME","MID_OPEN","BID", "OFFER","CHANGE","CHANGE_PCT","HIGH","LOW"]
        )
        
        self.executor = ThreadPoolExecutor(max_workers=config.THREADS)

        # Adding the "on_item_update" function to Subscription
        # self.subscription.addlistener(lambda item: self.executor.submit(event_handler,item))
        self.subscription.addlistener(event_handler)

        # Registering the Subscription
        self.sub_key = self.ls_client.subscribe(self.subscription)

        logger.info("Subscription:%s" % self.sub_key)


    
        

