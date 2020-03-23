const Dealer=require('./dealer')
const config=require('./load_config')


function random(seed) {
    var x = Math.sin(seed) * 10000;
    return x - Math.floor(x);
}

const test=async ()=>{
    try{
        const dealer=new Dealer(config)

        await dealer.connect()

        const test_db=dealer.client.db('test_db')

        const test_collection=test_db.collection('test_collection')

        let iterator=Array.from(Array(10).keys())
        let records=iterator.map((x)=>{
            return {type:'buy',
                    price:Math.random()}
        })
        console.log(records)
    
        await test_collection.insertMany(records)

        /* bulkWrite example */
        /*
        let query_result=test_collection.find({
            price:{$gte: 0.5}
        })

        let updates=[]
        
        await query_result.forEach(x=>{
            console.log(x)
            let update={ 
                updateOne: {
                    filter:{_id:x._id},
                    update:{ $set: {
                        update:true
                    }}
                }
            }
            updates.push(update) 
        })

        await test_collection.bulkWrite(updates)
        */

        /* updateMany example */

        let updateResult=await test_collection.updateMany(
            {price:{$gte: 0.5}},
            {
                $set: {
                    updated:true
                }
            }
        )

        console.log('Done')
    }
    catch(e){
        console.error(e)
    }



}

test()

