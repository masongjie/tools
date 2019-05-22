#!/usr/bin/env python  
#-*- coding:utf-8 -*-

import requests
from hashlib import md5
import time
import base64
import json


#用户id
ACCOUNT =""
#APP_id
APP_ID = ""
#认证组件
AUTH_TOKEN = ""

url = "https://app.cloopen.com:8883/2013-12-26/Accounts/{}/SMS/TemplateSMS".format(ACCOUNT)



def send_msg(iphone,templateId,data):
    '''
    iphone 接受方的电话号码
    templateId 模板id
    data  按照模板填入的列表
    返回值 True发送成功，False 发送失败
    '''

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
        "templateId":templateId,
        "datas":data
    }
    resp = requests.post(url,params=params,headers=headers,json=data)
    return json.loads(resp.text)["statusCode"]=="000000"


