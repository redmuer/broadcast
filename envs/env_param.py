#coding: UTF-8
import http.client
import json


class env:
    root_dir = ''
    wx_tocken = None

    wx_jsapi_ticket = None

    @classmethod
    def get_wx_token(cls):
        if None == cls.wx_tocken:
            cls.wx_tocken = cls.https_wx_token()

        print("token : ",cls.wx_tocken)
        return cls.wx_tocken

    @classmethod
    def get_wx_jsapi_ticket(cls):
        if None == cls.wx_jsapi_ticket:
            cls.wx_jsapi_ticket = cls.https_wx_jsapi_ticket()

        print("jsapi_ticket : ", cls.wx_jsapi_ticket)
        return cls.wx_jsapi_ticket

    @classmethod
    def https_wx_token(cls):
        conn = http.client.HTTPSConnection("api.weixin.qq.com")
        conn.request("GET",
                     '/cgi-bin/token?grant_type=client_credential&appid=wx55c990a2c8dcf77b&secret=8921f0cc72b4e6eb1170828ae4cdea6c')

        res = conn.getresponse()
        result = str(res.read(), encoding='utf8')
        print("wx_tocken : ", result)

        result = json.loads(result)

        return result['access_token']

    @classmethod
    def https_wx_access_tocken(self, code):
        conn = http.client.HTTPSConnection("api.weixin.qq.com")

        print(code,"code")

        conn.request("GET",
                     '/sns/oauth2/access_token?appid=wx55c990a2c8dcf77b&secret=8921f0cc72b4e6eb1170828ae4cdea6c&code=%s&grant_type=authorization_code' % (code))
                     # '/cgi-bin/token?grant_type=client_credential&appid=wx55c990a2c8dcf77b&secret=8921f0cc72b4e6eb1170828ae4cdea6c&code=%s&grant_type=authorization_code' % (code))
        # https: // api.weixin.qq.com / sns / oauth2 / access_token?appid = APPID & secret = SECRET & code = CODE & grant_type = authorization_code
        urllib.request.urlopen(get_team_id_url + team_id)
        res = conn.getresponse()
        print("res : ", res)
        result = str(res.read(), encoding='utf8')
        print("wx_access_token : ", result)

        result = json.loads(result)

        return result['openid']

    @classmethod
    def https_wx_jsapi_ticket(cls):
        token = cls.get_wx_token()

        conn = http.client.HTTPSConnection("api.weixin.qq.com")
        conn.request("GET",
                     '/cgi-bin/ticket/getticket?access_token=%s&type=jsapi' % (token))

        res = conn.getresponse()
        result = str(res.read(), encoding='utf8')
        print("wx_jsapi_ticket : ", result)

        result = json.loads(result)

        return result['ticket']