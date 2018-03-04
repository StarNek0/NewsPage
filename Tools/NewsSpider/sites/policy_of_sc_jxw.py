# coding:utf8
"""
--------------------------------------------------------------------------
    File:   policy_of_sc_jxw.py
    Auth:   zsdostar
    Date:   2018/3/4 17:56
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
        if x==1:
            url = u'http://ypt.scjm.gov.cn/scjxw/ggtz/common_list.shtml'
        else:
            url = u'http://ypt.scjm.gov.cn/scjxw/ggtz/common_list_%d.shtml' % x

        p = (requests.get(url)).content.decode('utf-8')
        root = etree.HTML(p)

        titles = root.xpath('//div[@class="List-T fl"]/a/text()')
        hrefs = root.xpath('//div[@class="List-T fl"]/a/@href')
        dates = root.xpath('//div[@class="div_w"]/h1/span/text()')
        # print titles
        for i in xrange(len(titles)):
            # print ToUni(pat,ti,titles[i].encode('unicode-escape'))
            if u'申报' in titles[i] and u'通知' in titles[i]:
                this_url = u'http://ypt.scjm.gov.cn/'+hrefs[i]
                dates[i] = dates[i].strip()
                # print titles[i], this_url,dates[i]

                cur = db.cursor()
                sql = "select count(*) from news_gov_msg where url='%s'" % this_url
                cur.execute(sql)
                res_of_select = cur.fetchone()[0]
                if res_of_select:
                    print 'This title has existed in the database.'
                    cur.close()
                else:
                    ccont = requests.get(this_url).content.decode('utf-8')
                    rroot = etree.HTML(ccont)
                    from_gov = rroot.xpath('//div[@class="source fl"]/text()')[0]
                    res = re.search(u'信息来源：(.+)', from_gov)
                    if res:
                        res = res.groups()[0]
                        sql = "insert into news_gov_msg(title, url, msg_date, site_from, msg_from) VALUES ('%s','%s','%s','%s','%s')" % (
                            titles[i], this_url, dates[i], u'四川经信委', res)
                        print titles[i], dates[i], this_url, res
                    else:
                        sql = "insert into news_gov_msg(title, url, msg_date, site_from, msg_from) VALUES ('%s','%s','%s','%s','%s')" % (
                            titles[i], this_url, dates[i][1:-1], u'四川经信委', u'四川经信委')
                        print titles[i], dates[i], this_url

                    cur.execute(sql)
                    db.commit()
                    cur.close()

    db.close()


if __name__ == '__main__':
    import policy_update
    policy_update.main()
    main()