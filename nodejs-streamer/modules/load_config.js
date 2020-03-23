

const config={
    IG_BASE_URL:'https://demo-api.ig.com/gateway/deal',
    MONGODB_URL:'mongodb://localhost:27017',
    LOGLEVEL:process.env.LOGLEVEL,
    REGION:process.env.REGION,
    SECRET_NAME:process.env.SECRET_NAME,
    S3_BUCKET_NAME:process.env.S3_BUCKET_NAME,
    EPIC:"CS.D.BITCOIN.CFD.IP",
    POINT_VALUE:1,
    MAX_RECORDS:100,
    DEFAULT_LIMIT:1,
    DEFAULT_STOP:1

}

/*

MINIMUM_STOP=4
MAXIMUM_STOP=100
MINIMUM_LIMIT=1
MAXIMUM_LIMIT=100

BUCKET=os.environ['S3_BUCKET_NAME']
SECRET=os.environ['SECRET_NAME']
*/

module.exports=config