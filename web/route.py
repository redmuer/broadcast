#coding: UTF-8

import sys
import os
from flask import Flask
from flask import render_template, request, jsonify, session, redirect, url_for
from db.db_app import db_utils
from envs.env_param import env
from db.bill import bill_proxy
from db.product import product_proxy
from db.bill_access import bill_access_proxy
from db.wx import Sign
import hashlib
import threading
import datetime

import json

app = Flask(__name__)
app.config["SECRET_KEY"] = 'M_TEST'

def session_check(session):
    if session.get('username'):
        return True
    else:
        return False

global start_long
def fun_timer():

    global  start_long
    start_long = start_long + 5
    if start_long > 7000:
        env.wx_tocken = None

    global timer
    timer = threading.Timer(5., fun_timer)
    timer.start()

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

@app.route('/bill/reserve', methods=['POST'])
def reserve_product():
    '''
    海报预约产品
    :return:
    '''
    json_data = json.loads(request.get_data(as_text=True))
    print(json_data)

    proxy = product_proxy()
    proxy.reserve_product(json_data)

    result = {"error_code":"0"}

    return jsonify(result)
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
        return jsonify({'error_code' : "0"})
    else:
        print('NO')
        result = {'error_code' : "1"}
        return jsonify(result)

#------------------------微信--------------------#

#@app.route('/weixin/js_token',methods=['POST'])
# def wexin_js_token():
#     '''
#     生成微信JS-JDK所需的认证
#     :return:
#     '''
#     data = request.get_data(as_text=True)
#     json_data = json.loads(data)
#     print("json_data",json_data)
#     url = json_data["url"]
#     print("wexin_js_token : url -- ",url)
#     jsapi_ticket = env.get_wx_jsapi_ticket()
#
#     sign = Sign(jsapi_ticket, url)
#     result = sign.sign()
#     print("ret signature : ",result)
#     return jsonify(result)

@app.route('/weixin/auth', methods=['GET'])
def weixin_auth():
    '''
    用来认证微信的后台Token
    :return:
    '''
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


@app.route('/test',methods=['GET'])
def test():
    return render_template('/bill/wx_test6.html',_bill_id='xxx',_pull_id='yyy',_open_id='zzz')

@app.route('/static/bill', methods=['GET'])
def weixin_snspi():
    '''
    网页授权认证
    :return:
    '''

    print("request.args ： ",request.args)

    bill_id = request.args.get("bill_id")
    pull_id = request.args.get("pull_id")
    # bill_pull_id = request.args.get("state")
    wx_code = request.args.get("code")

    tocken_result = env.https_wx_access_tocken(wx_code)

    if "errcode" in tocken_result:
        return redirect('https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx55c990a2c8dcf77b&redirect_uri=http%3A%2F%2Fwx1.lbikechina.com%2Fstatic%2Fbill%3Fbill_id%3De8226b69-336e-4e47-af25-dd959abad8a5%26pull_id%3Dpull3&response_type=code&scope=snsapi_userinfo&state=3#wechat_redirect')

    open_id = tocken_result['openid']

    print("open_id",open_id)

    param = {
        "bill_id":bill_id,
        "bill_pull_id":pull_id,
        "open_id":open_id
    }

    proxy = bill_access_proxy()
    proxy.save_access(param)

    print('bill_id',bill_id)
    print('pull_id',pull_id)
    print('open_id',open_id)

    ## 为页面商品赋值，本应该从后台取值，这里为了简化，直接写在页面中，仅把pull_id,bill_id和open_id穿进去
    send_url = ''
    if pull_id == 'pull1':
        send_url = '/bill/pull1.html'
    else:
        send_url = '/bill/pull2.html'

    return render_template(send_url,_bill_id=bill_id,_pull_id=pull_id,_open_id=open_id)
    # return app.send_static_file('wx_test5.html')
    # return redirect('/static/wx_test5.html')

if __name__ == '__main__':
    print(sys.argv[0])
    env.root_dir = sys.argv[0][0:-12]
    env.db_dir = sys.argv[0][0:-22]
    print("env.db_dir : ",env.db_dir)
    db_utils = db_utils()
    start_long = 0
    timer = threading.Timer(1, fun_timer)
    # timer.start()

    # env.get_wx_jsapi_ticket()

    app.run(host='0.0.0.0',port=80 , debug=True, use_reloader=False)