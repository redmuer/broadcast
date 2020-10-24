#coding: UTF-8


import threading
import uuid
from .db_app import db_utils
from datetime import datetime

class pull_proxy(object):
    _instance_lock = threading.Lock()

    _instance = None

    def __new__(cls, *args, **kwargs):
        if None == cls._instance:
            with pull_proxy._instance_lock:
                if None == cls._instance:
                    pull_proxy._instance = super().__new__(cls)

        return product_proxy._instance

    def __init__(self):
        pass


