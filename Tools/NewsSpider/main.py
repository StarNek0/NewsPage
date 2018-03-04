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

from sites import policy_of_gaoxin
from sites import policy_of_cd_tech
from sites import policy_of_cd_jxw
from sites import policy_of_sc_jxw
from sites import policy_of_sc_tech
from sites import policy_update

while True:
    # 项目申报
    try:
        policy_of_gaoxin.main()
        policy_of_cd_tech.main()
        policy_of_cd_jxw.main()
        policy_of_sc_jxw.main()
        policy_of_sc_tech.main()
        policy_update.main()

    except Exception as e:
        with open('policy.txt', 'w+') as f:
            f.write(str(e))

    # 打分
    try:
        db = pymysql.connect(host="localhost", user="root", password="klxsxzsdf1", db="newsspider", port=3306,
                             charset='utf8')
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
    except Exception as e:
        with open('score.txt', 'w+') as f:
            f.write(str(e))

    # 爬虫
    try:
        DATE1 = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        DATE2 = time.strftime('%Y-%m-%d', time.localtime(time.time() - 24 * 3600))
        wulianchina.DATE = DATE1
        wulianchina.main()
        ofweek.DATE = DATE2
        ofweek.main()
    except Exception as e:
        with open('craw.txt', 'w+') as f:
            f.write(str(e))

    time.sleep(3 * 3600)
