#coding: UTF-8
import http.client
import json


class env:
    root_dir = ''
    wx_tocken = None

    @classmethod
    def get_wx_tocke(cls):
        print("test")
        if None == cls.wx_tocken:
            cls.wx_tocken = cls.https_wx_tocken()

        return cls.wx_tocken


    @classmethod
    def https_wx_tocken(cls):
        conn = http.client.HTTPSConnection("api.weixin.qq.com")
        conn.request("GET",
                     '/cgi-bin/token?grant_type=client_credential&appid=wx55c990a2c8dcf77b&secret=8921f0cc72b4e6eb1170828ae4cdea6c')

        res = conn.getresponse()
        result = str(res.read(), encoding='utf8')
        print("wx_tocken : ", result)

        result = json.loads(result)

        return result['access_token']