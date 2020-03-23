const choose=(choices)=> {
    var index = Math.floor(Math.random() * choices.length);
    return choices[index];
  }

class Bidder{
    constructor(behaviour,config){
        this.DEFAULT_LIMIT=config.DEFAULT_LIMIT? config.DEFAULT_LIMIT:10
        this.DEFAULT_STOP=config.DEFAULT_STOP? config.DEFAULT_STOP:10
        this.behaviour=behaviour;
        // e.g. behaviour:
        // {   order_type: 'buy '}
    }

    order(){
        let order={
            type:("order_type" in this.behaviour)? this.behaviour.order_type:choose(['buy','sell']),
            stop:this.DEFAULT_STOP,
            limit:this.DEFAULT_LIMIT
        }

        return order
    }

}

module.exports=Bidder