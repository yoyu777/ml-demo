const AWS=require('aws-sdk')

AWS.config.region=process.env.REGION;



class Secret{
    constructor(){
        this.secretsmanager = new AWS.SecretsManager({apiVersion: '2017-10-17'});
        this.secret_name=process.env.SECRET_NAME;
    }

    async fetch(){
        var params = {
            SecretId: this.secret_name,
        };

        try{
            let response= await this.secretsmanager.getSecretValue(params).promise()
            const secrets=JSON.parse(response.SecretString)
            this.ig_identifier=secrets.ig_identifier
            this.ig_password=secrets.ig_password
            this.ig_api_key=secrets.ig_api_key
            return secrets
        }
        catch(e){
            console.error(e)
            return null
        }
        
    }
}

module.exports=Secret;