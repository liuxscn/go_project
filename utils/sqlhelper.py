import pymysql

def get_list(sql, args):
    conn = pymysql.connect(host='127.0.0.1', user='root', passwd='root', db='test', port=3306, charset='utf8')
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cur.execute(sql, args)
    db_data = cur.fetchall()
    cur.close()
    conn.close()

    return db_data


def get_one(sql, args):
    conn = pymysql.connect(host='127.0.0.1', user='root', passwd='root', db='test', port=3306, charset='utf8')
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cur.execute(sql, args)
    db_data = cur.fetchone()
    cur.close()
    conn.close()

    return db_data

def insert(sql, args):
    conn = pymysql.connect(host='127.0.0.1', user='root', passwd='root', db='test', port=3306, charset='utf8')
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cur.execute(sql, args)
    conn.commit()
    last_row_id = cur.lastrowid
    cur.close()
    conn.close()
    return last_row_id

def delete(sql, args):
    conn = pymysql.connect(host='127.0.0.1', user='root', passwd='root', db='test', port=3306, charset='utf8')
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cur.execute(sql, args)
    conn.commit()
    cur.close()
    conn.close()

def update(sql, args):
    conn = pymysql.connect(host='127.0.0.1', user='root', passwd='root', db='test', port=3306, charset='utf8')
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cur.execute(sql, args)
    conn.commit()
    cur.close()
    conn.close()

class SqlHelper(object):
    def __init__(self):
        #对象实例化时自动执行self.connect()
        self.connect()

    def connect(self):
        self.conn = pymysql.connect(host='127.0.0.1', user='root', passwd='root', db='test', port=3306, charset='utf8')
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def get_list(self, sql, args):
        self.cursor.execute(sql, args)
        result = self.cursor.fetchall()
        return result

    def get_one(self, sql, args):
        self.cursor.execute(sql, args)
        result = self.cursor.fetchone()
        return result

    def modify(self, sql, args):
        self.cursor.execute(sql, args)
        self.conn.commit()

    def multiple_modify(self, sql, args):
        self.cursor.executemany(sql, args)
        self.conn.commit()

    def create(self, sql, args):
        self.cursor.execute(sql, args)
        self.conn.commit()
        return self.cursor.lastrowid

    def close(self):
        self.cursor.close()
        self.conn.close()
