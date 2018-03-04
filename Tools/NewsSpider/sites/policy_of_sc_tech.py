# coding:utf8
"""
--------------------------------------------------------------------------
    File:   policy_of_sc_tech.py
    Auth:   zsdostar
    Date:   2018/3/4 16:54
    Sys:    Windows 10
--------------------------------------------------------------------------
    Desc:   
--------------------------------------------------------------------------
"""

import requests
import re
import time
import pymysql
import datetime

from lxml import etree


def main():
    db = pymysql.connect(host="localhost", user="root", password="klxsxzsdf1", db="newsspider", port=3306,
                         charset='utf8')
    for x in range(1,4):
        url = u'http://www.scst.gov.cn/tz/index_%d.jhtml' % x
        p = requests.get(url)
        cont = p.content
        root = etree.HTML(cont)

        titles = root.xpath('//div[@class="news_right mt10"]//h2/a/@title')
        hrefs = root.xpath('//div[@class="news_right mt10"]//h2/a/@href')
        dates = root.xpath('//div[@class="news_right mt10"]//h2/span/text()')

        for i in range(len(titles)):
            if u'申报' in titles[i] and u'通知' in titles[i]:
                this_url = u'http://www.scst.gov.cn/' + hrefs[i]


                cur = db.cursor()
                sql = "select count(*) from news_gov_msg where url='%s'" % this_url
                cur.execute(sql)
                res_of_select = cur.fetchone()[0]
                if res_of_select:
                    print 'This title has existed in the database.'
                    cur.close()
                else:
                    ccont = requests.get(this_url).content
                    rroot = etree.HTML(ccont)
                    from_gov = rroot.xpath('//div[@class="msgbar"]/text()')[1]
                    res = re.search(u'来源： (.+?) ',from_gov)
                    if res:
                        res = res.groups()[0]
                        sql = "insert into news_gov_msg(title, url, msg_date, site_from, msg_from) VALUES ('%s','%s','%s','%s','%s')" % (
                        titles[i], this_url, dates[i][1:-1], u'四川科技厅', res)
                        print titles[i], dates[i][1:-1], this_url,res
                    else:
                        sql = "insert into news_gov_msg(title, url, msg_date, site_from, msg_from) VALUES ('%s','%s','%s','%s','%s')" % (
                        titles[i], this_url, dates[i][1:-1], u'四川科技厅', u'四川科技厅')
                        print titles[i], dates[i][1:-1], this_url

                    cur.execute(sql)
                    db.commit()
                    cur.close()
    db.close()
if __name__ == '__main__':
    main()
