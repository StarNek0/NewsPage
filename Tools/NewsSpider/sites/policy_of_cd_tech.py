# coding:utf8
"""
--------------------------------------------------------------------------
    File:   policy_of_cd_tech.py
    Auth:   zsdostar
    Date:   2018/3/3 20:47
    Sys:    Windows 10
--------------------------------------------------------------------------
    Desc:   成都科技局项目申报爬虫
--------------------------------------------------------------------------
"""
import requests
import re
import time
import pymysql
import datetime

from lxml import etree

import sys
sys.path.append('../')

from company import COM, GOV


def DtCalc(stTime, edTime):
    st = time.mktime(time.strptime(stTime, "%Y-%m-%d"))
    ed = edTime

    return int((ed-st)/(24*3600))  # 时间差/天


def main():
    db = pymysql.connect(host="localhost", user="root", password="klxsxzsdf1", db="newsspider", port=3306,
                         charset='utf8')
    urls = [u"http://www.cdst.gov.cn/Type.asp?typeid=22&BigClassid=41&page=1",
                 u"http://www.cdst.gov.cn/Type.asp?typeid=22&BigClassid=41&page=2",
                 u"http://www.cdst.gov.cn/Type.asp?typeid=22&BigClassid=41&page=3",]

    for url in urls:
        cont =requests.get(url).content
        root = etree.HTML(cont)

        title = root.xpath('//li[@class="listli1"]/a/@title')
        href = root.xpath('//li[@class="listli1"]/a/@href')
        date = root.xpath('//li[@class="listli1"]/span/text()')
        for i in xrange(len(title)):
            if u'申报' in title[i] and u'通知' in title[i]:

                date[i] = date[i][1:-1]
                if DtCalc(date[i],time.time())<63:  # 两个月以内的信息
                    this_url = u'http://www.cdst.gov.cn/' + href[i]
                    print title[i], date[i], this_url, DtCalc(date[i], time.time()), '天'
                    this_cont = requests.get(this_url).content
                    this_root = etree.HTML(this_cont)

                    text = this_root.xpath('//div[@class="con_content"]/div[@align="center"]/text()')[1]
                    # print text
                    res = re.search(u'来源：(.+?)\n', text)

                    cur = db.cursor()
                    sql = "select count(*) from news_gov_msg where url='%s'" % this_url
                    cur.execute(sql)
                    res_of_select = cur.fetchone()[0]
                    if res_of_select:
                        print 'This title has existed in the database.'
                        cur.close()
                    else:
                        if res:
                            res = res.groups()[0]
                            sql = "insert into news_gov_msg(title, url, msg_date, site_from, msg_from) VALUES ('%s','%s','%s','%s','%s')" % (title[i], this_url, date[i],u'成都科技局',res)
                        else:
                            sql = "insert into news_gov_msg(title, url, msg_date, site_from, msg_from) VALUES ('%s','%s','%s','%s','%s')" % (title[i], this_url, date[i],u'成都科技局',u'成都科技局')

                        cur.execute(sql)
                        db.commit()
                        cur.close()

    db.close()

if __name__ == '__main__':
    main()

