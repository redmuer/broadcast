#coding: UTF-8

# import json
#
# aa = b'{"access_token":"38_SF28exAmNCFjs3V3EjOTlzBYea6iNNWQW7VWP2C-ZG387jrS5yfpexBQcHkXAMz2o9VCrBdxtPMCWWCVzG3k8DEgPT2BDuxRsRJE4Zk7m6mxY00e59y1jwaJ_0QtHVT15oELzlGTWZhBu34XYKEgAHASEY","expires_in":7200}'
#
# aa  = json.loads(str(aa, encoding='utf8'))
#
# print(aa["access_token"])

import time
import random
import string
import hashlib

class Sign:
    def __init__(self, jsapi_ticket, url):
        self.ret = {
            'nonceStr': self.__create_nonce_str(),
            'jsapi_ticket': jsapi_ticket,
            'timestamp': self.__create_timestamp(),
            'url': url
        }

    def __create_nonce_str(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))

    def __create_timestamp(self):
        return int(time.time())

    def sign(self):
        string = '&'.join(['%s=%s' % (key.lower(), self.ret[key]) for key in sorted(self.ret)])
        print(string)
        self.ret['signature'] = hashlib.sha1(string.encode("utf8")).hexdigest()
        return self.ret

if __name__ == '__main__':
    # 注意 URL 一定要动态获取，不能 hardcode
    # sign = Sign('jsapi_ticket', 'http://example.com')

    sign = Sign(jsapi_ticket, 'http://wx.lbikechina.com/static/wx_test.html')
    print("sign.sign",sign.sign())
