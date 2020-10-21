#coding: UTF-8

import sys
import os
from flask import Flask
from flask import render_template, request, jsonify, session, redirect, url_for
from db.db_app import db_utils
from envs.env_param import env
from db.bill import bill_proxy
from db.product import product_proxy
import hashlib

import json

app = Flask(__name__)
app.config["SECRET_KEY"] = 'M_TEST'

def session_check(session):
    if session.get('username'):
        return True
    else:
        return False

@app.route('/')
def hello_world():
    if session.get('username'):
        del session['username']
    return app.send_static_file('login.html')


@app.route('/index')
def index():
    check = session_check(session)
    if check:
        return app.send_static_file('m/index.html')
    else:
        return app.send_static_file('login.html')

# ------------------------海报路由 开始-------------------------
@app.route('/bill/index')
def show_bill_list():
    print('asdf')
    return app.send_static_file("m/article-list.html")


@app.route('/bill/list', methods=['POST'])
def get_bills():
    proxy = bill_proxy()
    bill_bases = proxy.get_sum_info()

    print('bill_bases',bill_bases)
    result = {
        "error_code":"0",
        "bills":json.dumps(bill_bases, default=lambda o: o.__dict__, sort_keys=True, indent=4),
        "recorders":len(bill_bases)
    }
    return jsonify(result)


@app.route('/bill/simple_list', methods=['POST'])
def get_bill_simple():
    proxy = bill_proxy()
    bills = proxy.get_bill_simple()
    print("bills",bills)
    result = {
        "error_code" : "0",
        "bills" : json.dumps(bills)
    }

    return jsonify(result)

@app.route('/bill/add', methods=['POST'])
def save_bill():
    json_data = json.loads(request.get_data(as_text=True))
    print(json_data)

    proxy = bill_proxy()
    proxy.save(json_data)

    return 'afdasdfasdff'
#------------------------海报路由 结束----------------------------

#------------------------商品路由 开始----------------------------


@app.route('/product/index')
def product_index():
    return app.send_static_file('m/product-list.html')


@app.route('/product/list',methods=['POST'])
def product_list():
    proxy = product_proxy()
    product_bases = proxy.get_all_product()

    print('product_bases', product_bases)
    result = {
        "error_code": "0",
        "products": json.dumps(product_bases, default=lambda o: o.__dict__, sort_keys=True, indent=4),
        "recorders": len(product_bases)
    }
    return jsonify(result)

@app.route('/product/add',methods=['POST'])
def product_add():
    json_data = json_data = json.loads(request.get_data(as_text=True))

    proxy = product_proxy()

    if proxy.save_product(json_data):
        result = result = {
            "error_code" : "0",
        }
    else:
        result = result = {
            "error_code": "1",
            "error_msg" : "保存错误"
        }
    return jsonify(result)
#------------------------商品路由 结束----------------------------

@app.route('/logon', methods=['POST'])
def logon():
    data = request.get_data(as_text=True)
    # data = request.json

    json_data = json.loads(data)

    user_name = json_data["username"]
    password = json_data["password"]

    print("user_name",user_name)

    print("password",password)
    if (user_name == 'm_test') and (password == 'zhengzhou'):
        print('OK')
        session['username'] = user_name
        return {'error_code' : "0"}
    else:
        print('NO')
        result = {'error_code' : "1"}
        return jsonify(result)

#------------------------微信认证--------------------

@app.route("/weixin/auth", method=['GET'])
def weixin_auth():
    signature = request.args.get('signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')
    echostr = request.args.get('echostr')
    token = "bill"
    tmpArr = [token, timestamp, nonce]
    tmpArr.sort()
    sha1 = hashlib.sha1()
    sha1.update(tmpArr[0].encode('utf-8'))
    sha1.update(tmpArr[1].encode('utf-8'))
    sha1.update(tmpArr[2].encode('utf-8'))
    hashcode = sha1.hexdigest()
    print("handle/GET func: hashcode, signature, timestamp, nonce, echostr, token: ", hashcode, signature, timestamp,
          nonce, echostr)
    if hashcode == signature:
        print("OKOK")
        return echostr
    else:
        pirnt("NO OK")
        return ""


if __name__ == '__main__':
    env.root_dir = sys.argv[0][0:-12]
    db_utils = db_utils()

    app.run(host='0.0.0.0',port=80)