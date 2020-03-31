const ls = require('lightstreamer-client-node');
// Lightstreamer Node.js Client 8.0.2 API Reference:
// https://lightstreamer.com/api/ls-nodejs-client/8.0.2/index.html


class Stream_Client{
    constructor(endpoint,identifier,CST,X_SECURITY_TOKEN){
        try{
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
              },
              onServerError:(e)=>{
                  console.error(e)
              }
            });
          this.client.connect()
        }
        catch(e){
          console.error(e)
        }
        
    }

    subscribe(epic,message_listener){
        try{
            // IG Streaming API Reference:
            // https://labs.ig.com/streaming-api-reference
            this.subscription = new ls.Subscription(
                "MERGE",
                ['MARKET:'+epic],
                ["UPDATE_TIME","BID","OFFER","CHANGE","CHANGE_PCT","MID_OPEN","HIGH","LOW","MARKET_STATE","MARKET_DELAY"]
            );
            
            this.subscription.addListener({
                onSubscription: function() {
                  console.info("SUBSCRIBED");
                },
                onUnsubscription: function() {
                  console.info("UNSUBSCRIBED");
                },
                onSubscriptionError: function (code, message) {
                    console.log('subscription failure: ' + code + " message: " + message);
                },
                onItemUpdate: function(item_object) {
                  try{
                      // Lightstreamer published some data
                      let item_json={}
                      item_object.forEachField(function (fieldName, fieldPos, value) {
                        item_json[fieldName]=value
                        // Alternatively, if the field is JSON, such as in a confirm message:
                        // var confirm = JSON.parse(value);
                        // console.log('json: ' + confirm.dealId)
                      })

                      const float_fields=['BID','OFFER','CHANGE','CHANGE_PCT','MID_OPEN','HIGH','LOW']
                      float_fields.every(float_filed=>item_json[float_filed]=parseFloat(item_json[float_filed]))
                    
                      console.debug(JSON.stringify(item_json))
                      message_listener(item_json)
                  }catch(e){
                    console.error(e)
                  }
                }
              });
              
            this.client.subscribe(this.subscription);
          }catch(e){
            console.error(e)
          }
    }
}

module.exports=Stream_Client

