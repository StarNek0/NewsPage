# coding:utf8
"""
--------------------------------------------------------------------------
    File:   wulianchina.py
    Auth:   zsdostar
    Date:   2018/2/13 21:09
    Sys:    Windows 10
--------------------------------------------------------------------------
    Desc:   http://www.50cnnet.com/
            物联中国
--------------------------------------------------------------------------
"""
import requests
import re
import time
import pymysql

from lxml import etree

from ..company import COM,GOV

key_words_of_gov = GOV


def output_urls(in_urls):
    dic={0:u'资讯',1:u'产业',2:u'服务',3:u'应用'}
    for i in range(len(in_urls)):

        page_index = 1
        while True:
            page = requests.get(in_urls[i] + '%d.html' % page_index)
            root = etree.HTML(page.text)

            time_tags = root.xpath('//ul[@class="xx-lb"]/li/span/text()')
            time_tags_Stamp = [int(time.mktime(time.strptime(x, "%Y-%m-%d %H:%M:%S"))) for x in time_tags]
            a_tags = root.xpath('//ul[@class="xx-lb"]/li/a[2]/@href')

            # 计算这个页面上新闻的时间范围
            timeArrayMax = time.strptime(time_tags[0], "%Y-%m-%d %H:%M:%S")
            timeArrayMin = time.strptime(time_tags[-1], "%Y-%m-%d %H:%M:%S")
            timeStampMax = int(time.mktime(timeArrayMax))
            timeStampMin = int(time.mktime(timeArrayMin))

            if timeStampMin < DATE_Stamp:
                for x in xrange(len(time_tags_Stamp)):
                    if abs(time_tags_Stamp[x] - DATE_Stamp) <= 3600 * 24:
                        # out_urls['http://www.50cnnet.com/' + a_tags[i][1:]]=dic[i]
                        out_urls.append('%dhttp://www.50cnnet.com/' % i + a_tags[x][1:])  # 懒了，直接把表示类别的数字加到url字符串的第一位
                break
            else:
                page_index += 1


def get_pages(page_urls):
    db = pymysql.connect(host="localhost", user="root", password="klxsxzsdf1", db="newsspider", port=3306, charset='utf8')

    dic = {0: u'资讯', 1: u'产业', 2: u'企业', 3: u'应用', 4:u'政策'}
    for page_url in page_urls:
        page_type = int(page_url[0])
        page_url = page_url[1:]
        print page_url
        try:
            page_html = requests.get(page_url)
            if page_html.status_code==404:
                continue
            root = etree.HTML(page_html.text)

            from_site = root.xpath('//div[@class="jia-chu"]/span/text()')[0][3:]
            print from_site

            page_date = root.xpath('//div[@class="xx-riqi"]/span[2]/text()')[0][3:13]
            print page_date

            whole_page = root.xpath('string(//div[@class="xx-nrzi"])').strip()
            print whole_page
            theme = re.search(u'.+\u3002', whole_page[0:165]).group()

            for company in COM:
                if whole_page[0:55].find(company)>0:
                    page_type=2

            for key_word in key_words_of_gov:
                if whole_page[0:55].find(key_word)>0:
                    print key_word, '---', whole_page[0:55]
                    page_type=4


            cur = db.cursor()
            sql = "select count(*) from news_news where theme='%s'" % theme
            cur.execute(sql)
            res = cur.fetchone()[0]
            if res:
                print res
                cur.close()
                continue


            sql = "insert into news_news(source_site,content,source_url,page_date,tag,theme) values('%s','%s','%s','%s','%s', '%s')" % (from_site, whole_page, page_url, page_date, dic[page_type], theme)
            cur.execute(sql)

            db.commit()
            cur.close()
        except Exception as e:
            print e


    db.close()


DATE = ''


def main():
    global DATE_Array, DATE_Stamp, in_urls, out_urls
    DATE_Array = time.strptime(DATE, '%Y-%m-%d')
    DATE_Stamp = int(time.mktime(DATE_Array))
    in_urls = ['http://www.50cnnet.com/list-6-', 'http://www.50cnnet.com/list-22-', 'http://www.50cnnet.com/list-15-',
               'http://www.50cnnet.com/list-84-']
    out_urls = []

    output_urls(in_urls)
    get_pages(out_urls)
