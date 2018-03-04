# coding:utf8
"""
--------------------------------------------------------------------------
    File:   policy_update.py
    Auth:   zsdostar
    Date:   2018/3/4 14:37
    Sys:    Windows 10
--------------------------------------------------------------------------
    Desc:   
--------------------------------------------------------------------------
"""
import pymysql
import time
db = pymysql.connect(host="localhost", user="root", password="klxsxzsdf1", db="newsspider", port=3306,
                     charset='utf8')
cur = db.cursor()
sql = "select id,msg_date,float_date from news_gov_msg;"
cur.execute(sql)
res = cur.fetchall()
for x in res:
    if x[2] == 0 or x[2] is None:
        float_date = time.mktime(time.strptime(x[1], "%Y-%m-%d"))
        cur.execute("update news_gov_msg set float_date=%f where id=%d" % (float_date,x[0]))
        print x[0],float_date
        db.commit()
cur.close()
db.close()