const Dealer=require('./dealer')
const config=require('./load_config')


function random(seed) {
    var x = Math.sin(seed) * 10000;
    return x - Math.floor(x);
}

const insertMany=async (test_collection)=>{
    
    try{
        let iterator=Array.from(Array(10).keys())
        let records=iterator.map((x)=>{
            return {type:'buy',
                    price:Math.random()}
        })
        console.log(records)
        
        await test_collection.insertMany(records)
    }
    catch(e){
        console.error(e)
    }
}

const bulkWrite=async (test_collection)=>{
    try{
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
                        updated:true
                    }}
                }
            }
            updates.push(update) 
        })
    
        await test_collection.bulkWrite(updates)
    }
    catch(e){
        console.error(e)
    }
   
}

const updateMany=async (dealer)=>{
    let updateResult=await test_collection.updateMany(
        {price:{$gte: 0.5}},
        {
            $set: {
                updated:true
            }
        }
    )
}

const test=async ()=>{
    try{
        const dealer=new Dealer(config)

        await dealer.connect()

        const test_db=dealer.client.db('test_db')

        const test_collection=test_db.collection('test_collection')

        insertMany(test_collection)

        bulkWrite(test_collection)
        
        let max=await test_collection.find({'updated':true}).sort('price',-1).limit(1).toArray()
        let min=await test_collection.find({'updated':true}).sort('price',1).limit(1).toArray()
        
        

        console.log('Done')
    }
    catch(e){
        console.error(e)
    }



}

test()

