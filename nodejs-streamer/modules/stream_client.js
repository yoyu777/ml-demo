const ls = require('lightstreamer-client-node');
// Lightstreamer Node.js Client 8.0.2 API Reference:
// https://lightstreamer.com/api/ls-nodejs-client/8.0.2/index.html


class Stream_Client{
    constructor(endpoint,identifier,CST,X_SECURITY_TOKEN){
        // IG Streaming API Guide:
        // https://labs.ig.com/streaming-api-guide
        this.client= new ls.LightstreamerClient(endpoint);  
        this.client.connectionDetails.setUser(identifier);
        this.client.connectionDetails.setPassword("CST-" + CST + "|XST-" +X_SECURITY_TOKEN);
        this.client.addListener({
            onListenStart: function() {
                console.info('ListenStart');
             },
            onStatusChange: function(newStatus) {         
                console.info(newStatus);
            }
          });
        this.client.connect()
    }

    subscribe(epic){
        // IG Streaming API Reference:
        // https://labs.ig.com/streaming-api-reference
        this.subscription = new ls.Subscription(
            "MERGE",
            [epic],
            ["UPDATE_TIME","BID","OFFER","CHANGE","CHANGE_PCT","MID_OPEN","HIGH","LOW","MARKET_STATE","MARKET_DELAY"]
        );
        
        this.subscription.addListener({
            onSubscription: function() {
              console.info("SUBSCRIBED");
            },
            onUnsubscription: function() {
              console.info("UNSUBSCRIBED");
            },
            onItemUpdate: function(obj) {
              console.info(obj.getValue("stock_name") + ": " + obj.getValue("last_price"));
            }
          });
          
        this.client.subscribe(this.subscription);
    }
}

module.exports=Stream_Client

