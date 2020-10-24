#coding: UTF-8

import threading
import uuid
from .db_app import db_utils
from datetime import datetime

class bill_access_proxy(object):

    _instance_lock = threading.Lock()

    _instance = None

    def __new__(cls, *args, **kwargs):
        if None == cls._instance:
            with bill_access_proxy._instance_lock:
                if None == cls._instance:
                    bill_access_proxy._instance = super().__new__(cls)

        return bill_access_proxy._instance

    def __init__(self):
        pass

    def save_access(self, json_data):
        sql = 'insert into bill_access values(?,?,?,?,?,?)'

        param = (
            str(uuid.uuid4()),
            json_data['bill_id'],
            json_data['bill_pull_id'],
            json_data['open_id'],
            datetime.now(),
            0
        )

        util = db_utils()
        try:
            util.exec_alone(sql, param)
            return True
        except Exception as err:
            print("err", err)
            return False