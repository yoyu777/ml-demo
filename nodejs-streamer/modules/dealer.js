const MongoClient = require('mongodb').MongoClient;

class Dealer{
    constructor(config){
        try{
            this.MAX_RECORDS=config.MAX_RECORDS? config.MAX_RECORDS:100;
            this.S3_BUCKET_NAME=config.S3_BUCKET_NAME;
            this.client = new MongoClient(config.MONGODB_URL,{ useUnifiedTopology: true });
            // To use the new Server Discover and Monitoring engine, 
            // pass option { useUnifiedTopology: true } to the MongoClient constructor.
            
            this.POINT_VALUE=config.POINT_VALUE;
            
            const AWS=require('aws-sdk')
            this.s3 = new AWS.S3({apiVersion: '2006-03-01'});
        }catch(e){
            console.error(e)
        }
        
    }
    async connect(){
        try{
            await this.client.connect()
            console.info("Connected successfully to MongoDB server");
            
            this.db= this.client.db('ml-demo')
            
            this.orders =this.db.collection('orders');
            this.orders.deleteMany({});
            this.orders.createIndexes([         //https://docs.mongodb.com/manual/reference/command/createIndexes/
                {
                    key:{
                        'stop_price':1
                        // 1 for ascending, -1 for descending
                    },
                    name:'stop_price_index'
                },
                {
                    key:{
                        'limit_price':1
                        // 1 for ascending, -1 for descending
                    },
                    name:'limit_price_index'
                },
                {
                    key:{
                        fulfilled:"hashed",
                    },
                    name:'fulfilled_index',
                    sparse:true
                }
            ])
            
            this.price=this.db.collection('price');
            this.price.deleteMany({});
            this.price.createIndex('timestamp')
            
            console.info('orders DB created')

            setInterval(this.export_fulfilled.bind(this),10*1000)

            console.info('Scheduled checking fulfilled records')

        }catch(e){
            console.error(e)
        }
    }
    
    process_order(order,bid,offer,timestamp){
        
        try{
            order.timestamp=timestamp;
        
            if (order.type=='buy'){
                order.price=offer;
                order.stop_price=offer-order.stop * this.POINT_VALUE;
                order.limit_price=offer+order.limit * this.POINT_VALUE;
            }else{
                order.price=bid;
                order.stop_price=bid+order.stop * this.POINT_VALUE;
                order.limit_price=bid-order.limit * this.POINT_VALUE;
            }
            this.orders.insertOne(order);
            console.debug('Successfully created an order')
        }
        catch(e){
            console.error(e)
        }
    }

    resolve_orders(bid,offer){
        try{
            let stop_triggered=this.orders.find({
                $and:[
                    {
                        "fulfilled": {$in: [null, false]},
                    },
                    {
                        $or:[{
                                $and:[
                                    {"type":"buy"},
                                    {"stop_price":{$gte:offer}}
                                ]
                            },
                            {
                                $and:[
                                    {"type":"sell"},
                                    {"stop_price":{$lte:bid}}
                                ]
                            }
                        ]
                    }
                ]
            },{
                hint: {stop_price:1}
            })

            let stop_updates=[]

            stop_triggered.forEach(x=>{
                console.debug(x)
                let loss_profit_factor=x.type=='buy'? 1 : -1
                let update={ 
                    updateOne: {
                        filter:{_id:x._id},
                        update:{ $set: {
                            "fulfilled":true,
                            "loss_or_profit":"loss",
                            "loss":x.stop_price-x.price*loss_profit_factor
                        }}
                    }
                }
                stop_updates.push(update) 
            },async ()=>{
                try{
                    if(stop_updates.length>0){
                        let result=await this.orders.bulkWrite(stop_updates)
                        console.debug(result.modifiedCount+' records updated')
                    }
                }
                catch(e){
                    console.error(e)
                }
                    
            })
            
            let limit_triggered=this.orders.find({
                $and:[
                    {
                        "fulfilled": {$in: [null, false]},
                    },
                    {
                        $or:[
                            {
                                $and:[
                                    {"type":"buy"},
                                    {"limit_price":{$lte:offer}}
                                ]
                            },
                            {
                                $and:[
                                    {"type":"sell"},
                                    {"limit_price":{$gte:bid}}
                                ]
                            }
                        ]
                    }
                ]
            },{
                hint: {limit_price:1}
            })

            let limit_updates=[]
            
            limit_triggered.forEach(x=>{
                console.debug(x)
                let loss_profit_factor=x.type=='buy'? 1 : -1
                let update={ 
                    updateOne: {
                        filter:{_id:x._id},
                        update:{ $set: {
                            "fulfilled":true,
                            "loss_or_profit":"profit",
                            "profit":x.limit_price-x.price*loss_profit_factor
                        }}
                    }
                }
                limit_updates.push(update) 
            },async ()=>{
                try{
                    if(limit_updates.length>0){
                        let result= await this.orders.bulkWrite(limit_updates)
                        console.debug(result.modifiedCount+' records updated')
                    }
                }catch(e){
                    console.error(e)
                }
                
            })
        
            
        }catch(e){
            console.error(e)
        }
        
        
    }
    
    
    log_price(message,timestamp){
        // Message example: {"UPDATE_TIME":"11:03:40","BID":"5918.21","OFFER":"5954.21",
        // "CHANGE":"-31.32","CHANGE_PCT":"-0.52","MID_OPEN":"5967.53","HIGH":"6177.00",
        // "LOW":"5885.50","MARKET_STATE":"TRADEABLE","MARKET_DELAY":"0"}
        try{
            message.timestamp=timestamp;
            this.price.insertOne(message);
            console.debug('Successfully logged a price')
        }
        catch(e){
            console.error(e)
        }
        
    }

    export_fulfilled(){
        try{

            if(!this.exporting){

                console.info('Checking fulfilled records...')

                let fulfilled=this.orders.find(
                    {
                        fulfilled:true,
                        exported:{$in: [null, false]}
                    },
                    {
                        hint: {fulfilled:"hashed"}
                    }
                )

                fulfilled.count()
                    .then(async count=> {
                        if(count>this.MAX_RECORDS){
                            try{
                                console.info('Exporting '+count+' records...')
                                this.exporting=true

                                let bucket=this.S3_BUCKET_NAME
                                let timestamp_now=Date.now()

                                // Exporting deals

                                let records=await fulfilled.toArray();
                                let headers=["timestamp","loss_or_profit","type","stop","limit","price","stop_price","limit_price"]

                                let updates=[]
                                let max_timestamp=Number.NEGATIVE_INFINITY,min_timestamp=Number.POSITIVE_INFINITY

                                let csv_data=records.map(record=>{
                                    updates.push({
                                        updateOne: {
                                            filter:{_id:record._id},
                                            update:{ $set: {
                                                "fulfilled":true,
                                                "exported":true
                                            }}
                                        }
                                    })

                                    max_timestamp=record.timestamp>max_timestamp?record.timestamp:max_timestamp
                                    min_timestamp=record.timestamp<min_timestamp?record.timestamp:min_timestamp

                                    let line_items=[]
                                    
                                    headers.map(header=>{
                                        line_items.push(JSON.stringify(record[header]))
                                    })

                                    let line=line_items.join(',')

                                    return line
                                })

                                let csv=csv_data.join('\n')
                            
                            
                                await this.s3.putObject({
                                    Body: csv, 
                                    Bucket: bucket, 
                                    Key: 'staging/deals-'+timestamp_now+'.csv'
                                }).promise()
                            

                                console.info('Exported deals as CSV')

                                
                                // Flagging deals as exported
                                let result= await this.orders.bulkWrite(updates)
                                console.info(result.modifiedCount+' records updated')

                                // Exporting prices
                                let prices=this.price.find(
                                    {   
                                        $and:[  
                                                {'timestamp': {$gte: min_timestamp-10*60*1000} },
                                                {'timestamp': {$lte: max_timestamp} },
                                        ]
                                    },
                                    {
                                        hint: {timestamp:1}
                                    }
                                )

                                let price_records=await prices.toArray()
                                
                                let price_csv_data=price_records.map(record=>{
                                    let headers=["timestamp","BID","OFFER","MID_OPEN","CHANGE","CHANGE_PCT","HIGH","LOW","UPDATE_TIME","MARKET_STATE","MARKET_DELAY"]

                                    let line_items=[]
                                    
                                    headers.map(header=>{
                                        line_items.push(JSON.stringify(record[header]))
                                    })

                                    let line=line_items.join(',')

                                    return line
                                })

                                let price_csv=price_csv_data.join('\n')

                                await this.s3.putObject({
                                    Body: price_csv, 
                                    Bucket: bucket, 
                                    Key: 'staging/price-'+timestamp_now+'.csv'
                                }).promise()

                                console.info('Exported prices as CSV')

                                this.exporting=false
                            }   // end try
                            catch(e){
                                console.error(e)
                            }   // end try catch

                        }   // end exporting
                    })  // end fulfilled.count
                .catch(e=>{
                    console.error(e)
                })
            }else{
                console.info('Still exporting...')
            }
            
        }catch(e){
            console.error(e)
        }
        
    }   // end export_fulfilled
}

module.exports=Dealer