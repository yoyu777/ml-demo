const request=require('request-promise-native')


class IG{
    constructor(config,identifier,password,api_key){
        this.IG_BASE_URL=config.IG_BASE_URL
        this.identifier=identifier
        this.password=password
        this.api_key=api_key
    }
    async login(){
        try{
            let options = {
                uri:this.IG_BASE_URL+'/session',
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


