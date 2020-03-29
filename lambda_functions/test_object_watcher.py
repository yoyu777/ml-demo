from object_watcher import run


event={
    "Records":[
        {"s3":{
            "object":{
                "key":"price-15853298627791.csv"
            }
        }}
    ]
}
run(event)

