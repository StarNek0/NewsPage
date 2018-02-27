# coding:utf8
"""
--------------------------------------------------------------------------
    File:   ofweek.py
    Auth:   zsdostar
    Date:   2018/2/13 17:58
    Sys:    Windows 10
--------------------------------------------------------------------------
    Desc:   http://iot.ofweek.com/
--------------------------------------------------------------------------
"""
import requests
import re
import pymysql

from lxml import etree

import sys
sys.path.append('../')
from company import COM

DATE = ''

# this_date = time.strftime('%Y-%m-%d',time.localtime(time.time()-3600*24))
key_words = [u'工信部', u'发改委', u'标准委', u'国务院', u'办公厅', u'科技部', u'版权局', u'运输部', u'卫计委', u'邮政局']

def spider(urls):
    db = pymysql.connect(host="localhost", user="root", password="klxsxzsdf1", db="newsspider", port=3306,charset='utf8')
    dic = {0: u'资讯', 1: u'产业', 2: u'企业', 3: u'应用', 4: u'政策'}

    for url in urls:
        try:
            page = requests.get(url)

            root = etree.HTML(page.text)

            heads = root.xpath('//div[@class="model_right model_right2"]/h3/a/text()')
            themes = root.xpath('//div[@class="model_right model_right2"]/p/span/text()')
            dates = []
            Dates = root.xpath('//div[@class="model_right model_right2"]/div[@class="tag"]/span[@class="date"]/text()')

            for i in Dates:
                i = re.findall('\d{4}-\d{2}-\d{2}', i)
                if i:
                    dates.append(i[0])

            for i in range(len(heads)):
                if dates[i] == DATE:
                    page_type = 0
                    print dates[i], themes[i]
                    for company in COM:
                        if themes[i].find(company) > 0:
                            page_type = 2

                    for key_word in key_words:
                        if themes[i].find(key_word) > 0:
                            print key_word, '---', themes[i]
                            page_type = 4
                    try:
                        cur = db.cursor()

                        sql = "select count(*) from news_news where theme like '%%%s%%'" % themes[i]

                        cur.execute(sql)
                        res = cur.fetchone()[0]
                        if res:
                            print 'ofweek:', res
                            cur.close()

                            continue

                        cur.execute("insert into news_news(theme,page_date,tag) values('%s','%s','%s')" % (themes[i], dates[i], dic[page_type]))
                        db.commit()

                        cur.close()
                    except Exception as e:
                        print e
        except Exception as e:
            print e

    db.close()


def main():
    urls = ['http://iot.ofweek.com/CAT-132219-smartindustry.html', 'http://iot.ofweek.com/CAT-132228-smartsafe.html',
            'http://iot.ofweek.com/CAT-132231-smarttele.html', 'http://iot.ofweek.com/CAT-132230-smartprotection.html',
            'http://iot.ofweek.com/CAT-132223-chelianwang.html', 'http://iot.ofweek.com/CAT-132218-smartcity.html',
            'http://iot.ofweek.com/CAT-132220-smartmedical.html',
            'http://iot.ofweek.com/CAT-132222-smartlogistics.html',
            'http://iot.ofweek.com/CATList-132200-8100-iot.html']
    spider(urls)
