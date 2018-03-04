# coding:utf8
"""
--------------------------------------------------------------------------
    File:   policy_of_cd_jxw.py
    Auth:   zsdostar
    Date:   2018/3/4 12:32
    Sys:    Windows 10
--------------------------------------------------------------------------
    Desc:   成都经信委项目申报爬虫，JS动态内容爬虫
--------------------------------------------------------------------------
"""
import requests
import re
import time
import pymysql
import datetime

from lxml import etree


def main():
    url = 'http://www.cdgy.gov.cn/newList1Level.jsp?classId=010501&firstNo=0105&num=null'

    h = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
        'Cookie': 'gwdshare_firstime=1520068960456; JSESSIONID=2C75B866B2F6C949795FDB534CF2EB65; _gscbrs_1405241782=1; _gscu_1405241782=20068960efrgjy55; Hm_lvt_61f86a9a2787e317b406b4d31819fd81=1520079527,1520079865,1520080678,1520137183; Hm_lpvt_61f86a9a2787e317b406b4d31819fd81=1520140155',
        }
    db = pymysql.connect(host="localhost", user="root", password="klxsxzsdf1", db="newsspider", port=3306,
                         charset='utf8')
    for i in range(1, 7):
        d = {'classId': '010501', 'SearchWord': 'null', 'p': str(i), 't': '0', }
        r = requests.post(url, data=d, headers=h)
        cont = r.content
        root = etree.HTML(cont)
        title = root.xpath('//li[@class="nctitle"]/a/@title')
        href = root.xpath('//li[@class="nctitle"]/a/@href')
        gov_and_date = root.xpath('//li[@class="ncother"]/text()')
        for x in range(len(title)):
            if u'申报' in title[x] and u'通知' in title[x]:
                gov = re.search(u'来源：(.+) ', gov_and_date[x]).group(1)
                date = re.search(u'发布时间：(.+)', gov_and_date[x]).group(1)
                site = u'成都经信委'
                this_url = u'http://www.cdgy.gov.cn/' + href[x]
                print title[x], this_url, gov, date

                cur = db.cursor()
                sql = "select count(*) from news_gov_msg where url='%s'" % this_url
                cur.execute(sql)
                res = cur.fetchone()[0]
                if res:
                    print title[x], 'has existed in the database.'
                    cur.close()
                else:
                    sql = "insert into news_gov_msg(title, url, msg_from, site_from, msg_date) VALUES ('%s','%s','%s','%s','%s')" % (title[x],this_url,gov,site,date)
                    cur.execute(sql)
                    db.commit()
                    cur.close()
    db.close()


if __name__ == '__main__':
    main()
