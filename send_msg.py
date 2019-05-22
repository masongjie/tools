#!/usr/bin/env python  
#-*- coding:utf-8 -*-

import requests
from hashlib import md5
import time
import base64
import json


#用户id
ACCOUNT ="8aaf07086ab0c082016ad93155371c82"
#APP_id
APP_ID = "8aaf07086ab0c082016ad93155831c88"
#认证组件
AUTH_TOKEN = "be42c2f1cf1f470e9d019cbcd2216683"

url = "https://app.cloopen.com:8883/2013-12-26/Accounts/{}/SMS/TemplateSMS".format(ACCOUNT)

def send_msg(iphone,data):

    time_str = time.strftime("%Y%m%d%H%M%S")

    SigParameter_str = ACCOUNT+AUTH_TOKEN+time_str
    # print(SigParameter_str)

    SigParameter = md5(SigParameter_str.encode(encoding="utf-8"))
    SigParameter = SigParameter.hexdigest().upper()

    params = {"sig":SigParameter}

    Authorization_str = ACCOUNT+":"+time_str
    Authorization = base64.b64encode(Authorization_str.encode("utf-8")).decode("utf-8")

    headers = {"Accept":"application/json",
               "Content-Type":"application/json;charset=utf-8",
               "Content-Length":"256",
               "Authorization":Authorization}


    data = {
        "to":iphone,
        "appId":APP_ID,
        "templateId":"1",
        "datas":data
    }
    resp = requests.post(url,params=params,headers=headers,json=data)
    return json.loads(resp.text)["statusCode"]=="000000"


