
import requests
import json
# Creating IGClient class

class IG_Client:
    def __init__(self,base_url,identifier,ig_password,ig_api_key):
        self.base_url=base_url
        self.identifier=identifier
        self.password=ig_password
        self.api_key=ig_api_key
        pass
def login(self):

    data={
        "identifier":self.identifier,
        "password":self.password
    }
    
    headers={
        "Content-Type":"application/json",
        "X-IG-API-KEY":self.api_key,
        "Version":"2"
    }
    
    r = requests.post(self.base_url+'/session',
        headers=headers,
        data=json.dumps(data))
    
    if r.status_code==200:
        self.CST=r.headers['CST']
        self.X_SECURITY_TOKEN=r.headers['X-SECURITY-TOKEN']
    
    return

IG_Client.login=login
def get_session_info(self):
    headers={
        "Content-Type":"application/json",
        "X-IG-API-KEY":self.api_key,
        "CST":self.CST,
        "X-SECURITY-TOKEN":self.X_SECURITY_TOKEN,
        "Version":"1"
    }
    
    r = requests.get(self.base_url+'/session',
        headers=headers)
        
    return r.json()

IG_Client.get_session_info=get_session_info