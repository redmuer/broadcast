#coding: UTF-8

# import json
#
# aa = b'{"access_token":"38_SF28exAmNCFjs3V3EjOTlzBYea6iNNWQW7VWP2C-ZG387jrS5yfpexBQcHkXAMz2o9VCrBdxtPMCWWCVzG3k8DEgPT2BDuxRsRJE4Zk7m6mxY00e59y1jwaJ_0QtHVT15oELzlGTWZhBu34XYKEgAHASEY","expires_in":7200}'
#
# aa  = json.loads(str(aa, encoding='utf8'))
#
# print(aa["access_token"])

# import time
# import random
# import string
# import hashlib
#
# class Sign:
#     def __init__(self, jsapi_ticket, url):
#         self.ret = {
#             'nonceStr': self.__create_nonce_str(),
#             'jsapi_ticket': jsapi_ticket,
#             'timestamp': self.__create_timestamp(),
#             'url': url
#         }
#
#     def __create_nonce_str(self):
#         return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))
#
#     def __create_timestamp(self):
#         return int(time.time())
#
#     def sign(self):
#         string = '&'.join(['%s=%s' % (key.lower(), self.ret[key]) for key in sorted(self.ret)])
#         print(string)
#         self.ret['signature'] = hashlib.sha1(string.encode("utf8")).hexdigest()
#         return self.ret
#
# if __name__ == '__main__':
#     # 注意 URL 一定要动态获取，不能 hardcode
#     # sign = Sign('jsapi_ticket', 'http://example.com')
#
#     sign = Sign("38_RkQ8ksGumhIrmJwG5MlVLUIyoBNgcWuU0Dvq3Acfm--VHMgkchLhbPgf3tiYdlPo9qyImTRoZGLq5wReZgQZ-hz0l5_Fcet_E460oYnr2LWSOOOFg0cGAZWsrvD0ZT8XqN1r1LNscOnJ7j99HIGfAGANOM", 'http://wx.lbikechina.com/static/wx_test.html')
#     print("sign.sign",sign.sign())

# import http.client
# import json
#
# conn = http.client.HTTPSConnection("api.weixin.qq.com")
# conn.request("GET",
#                      '/cgi-bin/ticket/getticket?access_token=%s&type=jsapi' % ('38_4hshUeHDE-q7_Phwj7_6sK5qHK9RhGYscUD5IPoD4VGLxbFFa_WVejSsqxi39WOrCJNjdT00Mi2YH2MsqZUhOzXemMBvmXMkoIu-vkR_i1KA94GwsiAOzluGmDlTUwiM7X-mSV6Pdo2QF1hCLXUcACAVHE'))
# res = conn.getresponse()
# result = str(res.read(), encoding='utf8')
# print("wx_jsapi_ticket : ", result)
#
# result = json.loads(result)
#
# print(result['ticket'])

# import time
# import random
# import string
# import hashlib
#
# class Sign:
#     def __init__(self, jsapi_ticket, url):
#         self.ret = {
#             'nonceStr': self.__create_nonce_str(),
#             'jsapi_ticket': jsapi_ticket,
#             'timestamp': self.__create_timestamp(),
#             'url': url,
#             'appid':'wx55c990a2c8dcf77b'
#         }
#
#     def __create_nonce_str(self):
#         return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))
#
#     def __create_timestamp(self):
#         return int(time.time())
#
#     def sign(self):
#         string = '&'.join(['%s=%s' % (key.lower(), self.ret[key]) for key in sorted(self.ret)])
#         print(string)
#         self.ret['signature'] = hashlib.sha1(string.encode("utf8")).hexdigest()
#         return self.ret
#
# from envs.env_param import env
#
# appId = "wx55c990a2c8dcf77b"
# jsapi_ticket = env.get_wx_jsapi_ticket()
# url = 'http://wx.lbikechina.com/static/wx_test5.html'
#
# sign = Sign(jsapi_ticket, url)
#
# sign.sign()
#
# print("sing.url" , sign.ret["url"])
# print("sing.nonceStr" , sign.ret["nonceStr"])
# print("sign.timestamp", sign.ret["timestamp"])
# print("sign.signature", sign.ret["signature"])


# url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxf0e81c3bee622d60&redirect_uri=http%3A%2F%2Fnba.bluewebgame.com%2Foauth_response.php&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect"
#
# import urllib.parse
# url_1="http://wx.lbikechina.com/static/bill"
# data=urllib.parse.quote(url_1)
# print(data)


#url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx55c990a2c8dcf77b&redirect_uri=http%3A%2F%2Fwx.lbikechina.com%2Fstatic%2Fbill&response_type=code&scope=snsapi_userinfo&state=3#wechat_redirect"

#url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx55c990a2c8dcf77b&redirect_uri=https%3A%2F%2Fwx.lbikechina.com%2Fstatic%2Fbill%3Fbill%3D1&response_type=code&scope=snsapi_base&state=3#wechat_redirect"


#http%3A%2F%2Fwx.lbikechina.com%2Fstatic%2Fbill%3Fbill%3D1


# import http.client
# conn = http.client.HTTPSConnection("api.weixin.qq.com")
# conn.request("GET",
#                      '/cgi-bin/token?grant_type=client_credential&appid=wx55c990a2c8dcf77b&secret=8921f0cc72b4e6eb1170828ae4cdea6c&code=011mbsGa19jHRz0qLaGa1fXsCq1mbsGV&grant_type=authorization_code')
#
#
# res = conn.getresponse()
# result = str(res.read(), encoding='utf8')
# print("wx_access_token : ", result)

# st = "authorization_code HTTP/1.1 200 OK"
# if st.find("authorization_code") == 0:
#     st = st[18:]
#
# print(st.split(None,2))

# print("authorization_code HTTP/1.1 200 OK".split(None,1))
# print('GET /static/bill?__debugger__=yes&cmd=resource&f=style.css HTTP/1.1" 200'.split(None, 2))

# import http.client
# conn = http.client.HTTPSConnection("www.jb51.net")
# conn.request("GET",'article/62726.htm')
#
# res = conn.getresponse()
#
# result = str(res.read(), encoding='utf8')
#
# print(result)

# authorization_code HTTP/1.1 200 OK
# HTTP/1.1 400 Bad Request

a = {'a':'1','b':'2'}
print(type(a))
print('a' in a)