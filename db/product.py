#coding: UTF-8


import threading
import uuid
from .db_app import db_utils
from datetime import datetime


class product_base:
    def __init__(self,row_data=None):
        if row_data:
            self.fid = row_data[0]
            self.bill_id = row_data[1]
            self.fname = row_data[2]
            self.url = row_data[3]
            self.total_count = row_data[4]
            self.revenue_count = row_data[5]
            self.price = row_data[6]
            self.bill_name = row_data[7]

        else:
            self.fid = None
            self.fname = None
            self.bill_id = None
            self.url = None
            self.total_count = 0
            self.revenue_count = 0
            self.price = 0.0
            self.bill_name = None

    def __repr__(self):
        return repr((self.fid, self.fname, self.bill_id, self.bill_name, self.url,
                     self.total_count, self.revenue_count, self.price))


class product_proxy(object):
    _instance_lock = threading.Lock()

    _instance = None

    def __new__(cls, *args, **kwargs):
        if None == cls._instance:
            with product_proxy._instance_lock:
                if None == cls._instance:
                    product_proxy._instance = super().__new__(cls)

        return product_proxy._instance

    def __init__(self):
        pass


    def save_product(self, json_data):
        '''
        保存一个产品
        :param json_data:
        :return:
        '''
        sql = 'insert into bill_commodity_base values(?,?,?,?,?,?,?)'

        param = (
            str(uuid.uuid4()),
            json_data['bill_id'],
            json_data['fname'],
            str(uuid.uuid4())[0:4],
            int(json_data['total_count']),
            0,
            float(json_data["price"])
        )

        util = db_utils()
        try:
            util.exec_alone(sql, param)
            return True
        except Exception as err:
            print("err", err)
            return False

    def reserve_product(self, json_data):
        sql = "insert into commodity_reserve values(?,?,?,?,?)"

        param = (
            str(uuid.uuid4()),
            json_data['product_id'],
            json_data['pull_id'],
            json_data['open_id'],
            datetime.now()
        )

        util = db_utils()
        util.exec_alone(sql,param)



    def get_product_by_bill(self, json_data = None):
        sql = 'select * from bill_commodity_base where bill_id = ?'
        param = (
            json_data['bill_id'],
        )

        util = db_utils()
        product_rows = util.select(sql, param)

        result = util.change_to_js(product_rows, ['fid', 'bill_id','fname','url','total_count','revenue_count','price'])

        return result

    def get_all_product(self, json_data=None):
        '''
        获得所有产品
        :param json_data:
        :return:
        '''
        sql = 'select a.*,b.fname from bill_commodity_base a,bill_base b where a.bill_id = b.fid and b.end_time>? and b.is_del = 0 order by b.fname'

        param = (
            datetime.now(),
        )

        util = db_utils()
        product_rows = util.select(sql, param)
        print('product_rows', product_rows)

        product_bases = []
        if len(product_rows) == 0:
            return product_bases
        else:
            for row in product_rows:
                product = product_base(row)
                product_bases.append(product)

        return product_bases



