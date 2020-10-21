import sqlite3
import threading
from envs.env_param import env


class db_utils:

    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(db_utils, "_instance"):
            with db_utils._instance_lock:
                if not hasattr(db_utils, "_instance"):
                    db_utils._instance = object.__new__(cls)
                    cls.table_init(cls)
        return db_utils._instance

    def __init__(self):
        pass

    def table_init(self):
        conn = sqlite3.connect('%s%s' % (env.root_dir, 'db/broadcast.db'))
        print('broadcast successfully')
        print('create table')
        sql_str = ''
        sql_path = '%s%s' % (env.root_dir,'db/migeration.sql')
        print('sql_path',sql_path)
        with open(sql_path, 'r') as f:
            sql_str = f.read()

        sqls = sql_str.split(';')

        c = conn.cursor()
        for sql in sqls:
            c.execute(sql)
            print('create table successfully')

        conn.commit()
        c.close()
        conn.close()

        return

    def exec_alone(self, sql, param):
        ### 执行一条语句
        cursor = None
        print('sql', sql)
        print('param', param)
        try:
            conn = sqlite3.connect('%s%s' % (env.root_dir, 'db/broadcast.db'))
            cursor = conn.cursor()
            cursor.execute(sql, param)
            conn.commit()
            cursor.close()
        finally:
            conn.close()
        return

    def exec_many(self, sql, params):
        # 执行许多语句
        pass


    def select(self,sql, param=(), columns=None):
        print('sql', sql)
        print('param', param)
        result = []
        if columns:
            result.append(columns)
        try:
            conn = sqlite3.connect('%s%s' % (env.root_dir, 'db/broadcast.db'))
            cursor = conn.cursor()
            st = cursor.execute(sql, param)
            for row in st:
                result.append(row)

            cursor.close()

        finally:
            conn.close()

        return result

    def change_to_js(self,rows,colums):
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