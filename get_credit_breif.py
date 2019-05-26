#!/usr/bin/env python  
#-*- coding:utf-8 -*-

import random
import time
import json
import rsa
import base64

class ask_zhimaxinyong():

    def __init__(self,appid,debug=True):
        self.appid = appid

        if debug:
            self.request_url = "https://openapi.alipaydev.com/gateway.do"
        else:
            self.request_url = "https://openapi.alipay.com/gateway.do"



    def get_transaction_id(self):
        transaction_id = ""
        for i in range(64):
            s = random.choice((random.randint(48, 57), random.randint(97, 122), 95))
            transaction_id += chr(s)
        return transaction_id

    def bulid_biz_content(self,cert_no,name,admittance_score):
        biz_content = {
            "transaction_id": self.get_transaction_id(),
            "product_code": "w1010100000000002733",
            "cert_type": "IDENTITY_CARD",
            "cert_no": cert_no,
            "name": name,
            "admittance_score": admittance_score,

        }
        return biz_content

    def build_params(self,cert_no,name,admittance_score):
        params = {
            "app_id": self.appid,
            "method": 'zhima.credit.score.brief.get',
            "charset": "utf-8",
            "sign_type": "RSA2",
            "timestamp": time.strftime('%Y-%m-%d %X'),
            "version": "1.0",
            "biz_content": json.dumps(self.bulid_biz_content(cert_no,name,admittance_score)),

        }
        sign_str = self.get_sign_str(params)
        sign = self.get_sign(sign_str)
        params['sign'] = sign
        return params

    def get_sign_str(self,params):
        params_list = [i for i in params]
        params_list = sorted(params_list)

        sign_str = ""
        for i in params_list:
            if isinstance(params[i], str):
                sign_str += i + "=" + params[i] + '&'
            elif isinstance(params[i], int):
                sign_str += i + "=" + str(params[i]) + '&'
            elif isinstance(params[i], dict):
                sign_str += i + "=" + json.dumps(params[i]) + '&'
        sign_str = sign_str[:-1]
        return sign_str

    def get_sign(self,sign_str):
        with open('keys/private.txt', 'r') as f:
            privkey = rsa.PrivateKey.load_pkcs1(f.read())

        sign_1 = rsa.sign(sign_str.encode('utf-8'), privkey, hash_method='SHA-256')

        # print("+"*50)
        sign = base64.b64encode(sign_1).decode('utf-8')
        return sign

    def ask_credit(self,params):
        import requests
        response = requests.get(self.request_url, params=params)
        return response.json()
