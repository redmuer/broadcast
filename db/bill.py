#coding: UTF-8

import threading
import uuid
from .db_app import db_utils
from datetime import datetime

class bill_base:
    def __init__(self):
        self.fid = None
        self.fname = None
        self.start_time = None
        self.end_time = None
        self.url = None
        self.build_time = None
        self.is_del = None

        self.group = 0
        self.total_click = 0
        self.total_reserve = 0
        self.total_amount = 0.

    def __repr__(self):
        return repr((self.fid, self.fname, self.start_time, self.end_time, self.url,
                     self.build_time, self.is_del, self.group, self.total_click,
                     self.total_reserve, self.total_amount))

class bill_pull:
    def __init__(self, row=None):
        if row:
            self.fid = row[0]
            self.bill_id = row[1]
            self.url_param = row[2]
            self.des = row[3]
            self.build_time = row[4]
            self.is_del = row[5]
        else:
            self.fid = None
            self.bill_id = None
            self.url_param = None
            self.des = None
            self.build_time = None
            self.is_del = None

    def __repr__(self):
        return repr((self.fid, self.bill_id, self.url_param, self.des, self.build_time, self.is_del))

class bill_proxy:

    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(bill_proxy, "_instance"):
            with bill_proxy._instance_lock:
                if not hasattr(bill_proxy, "_instance"):
                    bill_proxy._instance = object.__new__(cls)
        return bill_proxy._instance

    def __init__(self):
        pass


    def save(self,json_data):
        #保存一条海报记录
        sql = 'insert into bill_base values(?,?,?,?,?,?,?)'

        param = (
            str(uuid.uuid4()),
            json_data['bill_name'],
            datetime.strptime(json_data['start_time'], "%Y-%m-%d"),
            datetime.strptime(json_data['end_time'], "%Y-%m-%d"),
            str(uuid.uuid4())[0:4],
            datetime.now(),
            False
        )

        util = db_utils()
        try:
            util.exec_alone(sql, param)
            return True
        except Exception as err:
            print("err",err)
            return False

    def get_bill_simple(self, json_data = None):
        '''
        获得一个简单地bill
        :param json_data:
        :return:
        '''
        sql = "select fid,fname from bill_base where is_del=0 or end_time<? order by start_time"
        util = db_utils()

        bill_rows = util.select(sql,(datetime.now(),))

        result = util.change_to_js(bill_rows,['fid','fname'])

        return result


    def get_sum_info(self, json_data=None):
        '''
        获得海报汇总信息
        :param json_data:
        :return:
        '''
        sql1 = 'select * from bill_base where is_del=0 order by start_time asc'
        util = db_utils()

        bill_row = util.select(sql1)
        print('bill_row',bill_row)
        bill_bases = []
        if len(bill_row) == 0:
            return bill_bases

        for row in bill_row:
            bill = bill_base()
            bill.fid = row[0]
            bill.fname = row[1]
            bill.start_time = row[2]
            bill.end_time = row[3]
            bill.url = row[4]
            bill.build_time = row[5]
            bill.is_del = row[6]

            bill_bases.append(bill)

        for bill in bill_bases:
            sql = 'select * from bill_pull where bill_id = ?'
            param = (bill.fid,)

            bill_pulls = []
            bill_pull_rows = util.select(sql,param)
            if len(bill_pull_rows) == 0:
                bill.group = 0
                bill.total_click = 0
                bill.total_reserve = 0
                bill.total_amount = 0
            else:
                for row in bill_pull_rows:
                    pull = bill_pull(row)
                    bill_pulls.append(pull)
                #得到群数
                bill.group = len(bill_pulls)
                #计算总预约数
                bill.total_reserve = 0
                #计算商品价值
                bill.total_amount = 0.0
                for pull in bill_pulls:
                    sql = "select count(*) from bill_access where bill_pull_id = ?"
                    param = (pull.fid,)

                    count_row = util.select(sql, param)
                    bill.total_click = bill.total_click + count_row

                    #获取当前这个群的海报的商品预约情况
                    reserve_count = self.get_bill_reserve_count(pull.fid)
                    bill.total_reserve = bill.total_reserve + reserve_count

                    #获得群里的商品价值
                    amount = self.get_bill_amount(pull.fid)
                    bill.total_amount = bill.total_amount+amount

        return bill_bases

    def get_bill_reserve_count(self, pull_id):
        '''
        获取某个群的预约情况
        '''
        sql = 'select count(*) from commodity_reserve where bill_pull_id = ?'
        param = (pull_id,)

        util = db_utils()
        count_row = util.select(sql, param)

        if len(count_row) > 0:
            return count_row[0]
        else:
            return 0

    def get_bill_amount(self, pull_id):
        '''
        获取订单商品价值
        :param pull_id:
        :return:
        '''
        sql = 'select sum(b.price) from commodity_reserve a,bill_commodity_base b where a.bill_commodity_id = b.fid and a.bill_pull_id=?'
        param = (pull_id,)

        util = db_utils()
        count_row = util.select(sql, param)

        if len(count_row) > 0:
            return count_row[0]
        else:
            return 0

