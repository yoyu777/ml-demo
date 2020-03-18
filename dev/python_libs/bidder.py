from python_libs.loggers import logger
from python_libs import config
import random 

class Bidder:
    def __init__(self,id):
        self.id=id
        self.behaviour={}
        pass

    def set_behaviour(self,**kwargs):
        for key, value in kwargs.items(): 
            self.behaviour[key]=value

    def order(self):
        order_type=random.choice(['buy','sell']) if "order_type" not in self.behaviour else self.behaviour["order_type"]
        stop=random.randint(config.MINIMUM_STOP, config.MAXIMUM_STOP) if "stop" not in self.behaviour else self.behaviour["stop"]
        limit=random.randint(config.MINIMUM_LIMIT, config.MAXIMUM_LIMIT) if "limit" not in self.behaviour else self.behaviour["limit"] 
        return {
            "order_type":order_type,
            "stop":stop,
            "limit":limit
        }

