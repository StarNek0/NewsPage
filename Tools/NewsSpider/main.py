# coding:utf8
"""
--------------------------------------------------------------------------
    File:   main.py
    Auth:   zsdostar
    Date:   2018/2/13 17:42
    Sys:    Windows 10
--------------------------------------------------------------------------
    Desc:   
--------------------------------------------------------------------------
"""
import time
import pymysql

import sites.ofweek as ofweek
import sites.wulianchina as wulianchina
from sub_word.score_it import exam
while True:
    # 打分
    db = pymysql.connect(host="47.95.115.243", user="root", password="klxsxzsdf1", db="newsspider", port=3306,charset='utf8')
    cur = db.cursor()
    sql = "select id,score,theme from news_news GROUP BY theme"
    cur.execute(sql)
    whole_datas = cur.fetchall()
    cur.close()
    for data in whole_datas:
        if data[1] is None:
            cur = db.cursor()
            sql = 'update news_news set score=%d where id=%d' % (exam(data[2]), data[0])
            cur.execute(sql)
            db.commit()
            cur.close()
    db.close()


    # 爬虫
    # DATE1 = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    # DATE2 = time.strftime('%Y-%m-%d',time.localtime(time.time()-24*3600))
    # wulianchina.DATE = DATE1
    # wulianchina.main()
    # ofweek.DATE = DATE2
    # ofweek.main()

    time.sleep(3*3600)
