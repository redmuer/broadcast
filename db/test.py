#coding: UTF-8

# import json
#
# class Customer:
#     def __init__(self, name, grade, age, home, office):
#         self.name = name
#         self.grade = grade
#         self.age = age
#         self.address = Address(home, office)
#
#     def __repr__(self):
#         return repr((self.name, self.grade, self.age, self.address.home, self.address.office))
#
# class Address:
#     def __init__(self, home, office):
#         self.home = home
#         self.office = office
#     def __repr__(self):
#         return repr((self.name, self.grade, self.age))
#
# customers = [
#     Customer('john', 'A', 15, '111', 'aaa'),
#     Customer('jane', 'B', 12, '222', 'bbb'),
#     Customer('dave', 'B', 10, '333', 'ccc'),
# ]
#
# json_str = json.dumps(customers, default=lambda o: o.__dict__, sort_keys=True, indent=4)
#
# print(json_str)
# from flask import render_template, request, jsonify
# # result = {'error_code' : "1"}
# # print(type(result))
#
# import json
# def change_to_js(rows, colums):
#     '''
#     把行数据组装成为一个字典树组对象
#     :param rows:
#     :param colums:
#     :return:
#     '''
#     if len(rows) == 0:
#         return []
#
#     result = []
#
#     for row in rows:
#         row_dict = {}
#         for i in range(len(colums)):
#             row_dict[colums[i]] = row[i]
#
#         result.append(row_dict)
#
#     return result
#
# rows = [[1,'b'],[2,'d']]
# result = change_to_js(rows,['AA','BB'])
# print(json.dumps(result))

# import http.client
#
# # 1. 建立HTTP连接
# conn = http.client.HTTPSConnection("api.weixin.qq.com")
# # 2. 发送GET请求，制定接口路径
# conn.request("GET", '/cgi-bin/token?grant_type=client_credential&appid=wx55c990a2c8dcf77b&secret=8921f0cc72b4e6eb1170828ae4cdea6c')
# # 3. 获取相应
# res = conn.getresponse()
# # 4. 解析相应.进行解码
# print(res.read()) # 自己解码

import json

aa = b'{"access_token":"38_SF28exAmNCFjs3V3EjOTlzBYea6iNNWQW7VWP2C-ZG387jrS5yfpexBQcHkXAMz2o9VCrBdxtPMCWWCVzG3k8DEgPT2BDuxRsRJE4Zk7m6mxY00e59y1jwaJ_0QtHVT15oELzlGTWZhBu34XYKEgAHASEY","expires_in":7200}'

aa  = json.loads(str(aa, encoding='utf8'))

print(aa["access_token"])