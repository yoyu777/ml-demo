const console=require('./modules/logger')


const Secret=require('./modules/secret')
const secret=new Secret()


const IG=require('./modules/ig')
const Stream_Client=require('./modules/stream_client')

const main=async ()=>{
    await secret.fetch()
    const ig=new IG(secret.ig_identifier,secret.ig_password,secret.ig_api_key)
    const session = await ig.login()
    const stream_client=new Stream_Client(session.lightstreamerEndpoint,ig.identifier,ig.cst,ig.x_security_token)
    stream_client.subscribe("CS.D.BITCOIN.CFD.IP")
    console.log('OK')


}

main()
