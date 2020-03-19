from python_libs.loggers import logger, Deal_Logger
from python_libs import config
from pymongo import MongoClient

class Dealer:
    def __init__(self):
        self.orders = MongoClient('localhost', 27017).ml_lab.orders
        self.orders.delete_many({})
        self.orders.create_index([('stop_price', 1),('limit_price',1)])
        logger.info('orders DB created')
        self.deal_logger=Deal_Logger(config.EPIC)
        pass

    def process_orders(self,orders,bid,offer,timestamp):
        def process_order(order,timestamp):
            order['timestamp']=timestamp
            if order['order_type']=='buy':
                order['price']=offer
                order['stop_price']=offer-order['stop']*config.POINT_VALUE   
                order['limit_price']=offer+order['limit']*config.POINT_VALUE    
            else:
                order['price']=bid
                order['stop_price']=bid+order['stop']*config.POINT_VALUE
                order['limit_price']=bid-order['limit']*config.POINT_VALUE
            return order
        new_orders=[process_order(order,timestamp) for order in orders]
        self.add_orders(new_orders)
        self.resolve_orders(bid,offer)
        return

    def add_orders(self,new_orders):
        self.orders.insert_many(new_orders)
        logger.debug('%s new orders received' % len(new_orders) )
        return

    def calculate_deal(self,order,deal_type):
        loss_profit_factor=1 if order['order_type']=='buy' else -1
        if deal_type=='stop':
            loss_or_profit=(order['stop_price']-order['price'])*loss_profit_factor
        elif deal_type=='limit':
            loss_or_profit=(order['limit_price']-order['price'])*loss_profit_factor
        
        deal={
            'timestamp':order['timestamp'],
            'deal_type':deal_type,
            "order_type":order["order_type"],
            "stop":order["stop"],
            "limit":order["limit"],
            "price":round(order["price"],8),
            "stop_price":round(order["stop_price"],8),
            "limit_price":round(order["limit_price"],8),
            "loss_or_profit":round(loss_or_profit,8)
        }
        self.deal_logger.log(deal)
    
    def resolve_orders(self,bid,offer):
        stop_triggered=list(self.orders.find({
            "$or":[
                {
                    "$and":[
                        {"order_type":"buy"},
                        {"stop_price":{"$gte":offer}}
                    ]
                },
                {
                    "$and":[
                        {"order_type":"sell"},
                        {"stop_price":{"$lte":bid}}
                    ]
                }
            ]
        }))
        [self.calculate_deal(order,'stop') for order in stop_triggered]

        if(len(stop_triggered)>0):
            logger.info('%s stop orders triggered' % len(stop_triggered))

        limit_triggered=list(self.orders.find({
            "$or":[
                {
                    "$and":[
                        {"order_type":"buy"},
                        {"limit_price":{"$lte":bid}}
                    ]
                },
                {
                    "$and":[
                        {"order_type":"sell"},
                        {"limit_price":{"$gte":offer}}
                    ]
                }
            ]
        }))

        [self.calculate_deal(order,'limit') for order in limit_triggered]

        if(len(limit_triggered)>0):
            logger.info('%s limit orders triggered' % len(limit_triggered))

        to_be_deleted=[doc['_id'] for doc in stop_triggered]+[doc['_id'] for doc in limit_triggered]
        self.orders.delete_many({
            "_id":{"$in":to_be_deleted}
        })

        logger.debug(
            '%s orders completed. %s orders remain.' % 
            (
                len(to_be_deleted),
                self.orders.count_documents({})
            )
        )
        return

    
        