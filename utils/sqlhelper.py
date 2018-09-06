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
    cur.close()
    conn.close()

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


