# coding:utf8
"""
--------------------------------------------------------------------------
    File:   sub_word.py
    Auth:   zsdostar
    Date:   2018/2/28 1:21
    Sys:    Windows 10
--------------------------------------------------------------------------
    Desc:   
--------------------------------------------------------------------------
"""

import jieba
import jieba.posseg as psg
import pymysql
from collections import Counter

if __name__ =='__main__':
# try:
    # 获取源数据
    db = pymysql.connect(host="47.95.115.243", user="root", password="klxsxzsdf1", db="newsspider", port=3306,
                         charset='utf8')
    cur = db.cursor()
    sql = "select id,theme from news_news GROUP BY theme"
    cur.execute(sql)
    whole_datas = cur.fetchall()
    cur.close()

    #  分词
    jieba.load_userdict('user_dict.txt')
    d = []
    for data in whole_datas:
        d.append(data[1])
    data_string = u''.join(d)

    datas = {}
    for x in psg.cut(data_string):
        if len(x.word)>1:

            datas[x.word] = x.flag


    c = Counter([x for x in jieba.cut(data_string) if len(x) >= 2]).most_common(20000)
    count = 1
    for i in c:
        try:
            if datas[i[0]] not in ['v','m','c','p','d','c']:
                # print count, i[0], i[1], datas[i[0]]
                # count += 1
                print i[0],
        except:
            pass
# except Exception as e:
#     print e
# finally:
    db.close()
