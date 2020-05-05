

const config={
    IG_BASE_URL:'https://demo-api.ig.com/gateway/deal',
    MONGODB_URL:'mongodb://localhost:27017',
    LOGLEVEL:process.env.LOGLEVEL,
    REGION:process.env.REGION,
    SECRET_NAME:process.env.SECRET_NAME,
    S3_BUCKET_NAME:process.env.S3_BUCKET_NAME,
    EPIC:"CS.D.BITCOIN.CFD.IP",
    POINT_VALUE:1,
    MAX_RECORDS:10000,
    DEFAULT_LIMIT:20,
    DEFAULT_STOP:20

}

module.exports=config