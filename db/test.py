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
from flask import render_template, request, jsonify
# result = {'error_code' : "1"}
# print(type(result))

import json
def change_to_js(rows, colums):
    '''
    把行数据组装成为一个字典树组对象
    :param rows:
    :param colums:
    :return:
    '''
    if len(rows) == 0:
        return []

    result = []

    for row in rows:
        row_dict = {}
        for i in range(len(colums)):
            row_dict[colums[i]] = row[i]

        result.append(row_dict)

    return result

rows = [[1,'b'],[2,'d']]
result = change_to_js(rows,['AA','BB'])
print(json.dumps(result))