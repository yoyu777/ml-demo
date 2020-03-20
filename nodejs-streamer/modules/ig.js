const request=require('request-promise-native')

IG_ENDPOINT=process.env.IG_ENDPOINT



class IG{
    constructor(identifier,password,api_key){
        this.identifier=identifier
        this.password=password
        this.api_key=api_key
    }
    async login(){
        let options = {
            uri:IG_ENDPOINT+'deal/session',
            method: 'POST',
            headers: {
              'Content-Type': 'application/json; charset=UTF-8',
              'Version': 2,
              'X-IG-API-KEY':this.api_key,
              'Accept':'application/json; charset=UTF-8'
            },
            body:{
                identifier:this.identifier,
                password:this.password,
                encryptedPassword: 'null'
            },
            json:true,
            transform:(body,response)=>{
                return response
            }
          };
        try{
            let response= await request(options)
            this.session=response.body
            this.cst=response.headers.cst
            this.x_security_token=response.headers['x-security-token']
            return response.body
        }catch(e){
            console.error(e)
        }
        
    }

}

module.exports=IG


