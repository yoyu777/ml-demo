const config=require('./modules/load_config')
const console=require('./modules/logger')

const Secret=require('./modules/secret')
const secret=new Secret(config)


const IG=require('./modules/ig')
const Stream_Client=require('./modules/stream_client')

const Dealer=require('./modules/dealer')
const Bidder=require('./modules/bidder')


const main=async ()=>{
    try{
        await secret.fetch()
    
        const dealer= new  Dealer(config)
        await dealer.connect()

        const bidder=new Bidder({order_type:'buy'},config)

        const ig=new IG(config,secret.ig_identifier,secret.ig_password,secret.ig_api_key)
        const session = await ig.login()
        
        const stream_client=new Stream_Client(session.lightstreamerEndpoint,ig.identifier,ig.cst,ig.x_security_token)
        stream_client.subscribe("CS.D.BITCOIN.CFD.IP",(message)=>{
            console.debug('Received a message')
            
            const timestamp=Date.now()
            
            dealer.log_price(message,timestamp);
            
            let order=bidder.order()
            dealer.process_order(order,message.BID,message.OFFER,timestamp);
            
            dealer.resolve_orders(message.BID,message.OFFER)
            
            console.debug('Finished processing the message')
        })
        
        console.log('OK')

    }catch(e){
        console.error(e)
    }
    

}

main()
