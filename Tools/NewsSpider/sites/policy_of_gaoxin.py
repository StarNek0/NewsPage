# coding:utf8
"""
--------------------------------------------------------------------------
    File:   policy_of_gaoxin.py
    Auth:   zsdostar
    Date:   2018/2/27 18:34
    Sys:    Windows 10
--------------------------------------------------------------------------
    Desc:   成都高新区项目申报爬虫
--------------------------------------------------------------------------
"""
import requests
import re
import time
import pymysql

from lxml import etree

import sys
sys.path.append('../')
from company import COM, GOV


def get_urls(in_url):
    urls = []
    content = requests.get(in_url).content
    root = etree.HTML(content)

    # 获取该搜索结果的页数
    temp_text = root.xpath('//div[@class="text-center pagin mt20 pb20"]/div/text()')[0]
    index_num = int(re.search(u'/(\d+)页', temp_text).group(1))
    # 从每页获取每个标题的URL并存入urls中
    for i in range(1, index_num + 1):
        thispage_url = in_url.replace('/index.jhtml', '/index_%d.jhtml' % i)
        content = requests.get(thispage_url).content
        root = etree.HTML(content)

        each_title_urls = root.xpath('//tbody/tr/td/a/@href')
        urls.extend(each_title_urls)
    return urls


def get_each_gov_msg(every_page_url):
    db = pymysql.connect(host="localhost", user="root", password="klxsxzsdf1", db="newsspider", port=3306,
                         charset='utf8')
    for each_page_url in every_page_url:
        cid = re.search('(\d+)\.jhtml', each_page_url).groups(1)[0]
        content = requests.get(each_page_url).content
        root = etree.HTML(content)

        title = root.xpath('//div[@class="page"]/h1/text()')[0]
        date = root.xpath('//div[@class="sx col-md-6"]/span[1]/text()')[0]
        from_gov = root.xpath('//div[@class="sx col-md-6"]/span[2]/text()')[0]

        # 不清楚哪种存word比较好，故此都存下了，end_right_content_num是为了切割正文main_content和落款end_content的
        total_content = root.xpath('string(//div[@id="d_content"])')  # ！！！！！！！！！！！！！！！
        content = root.xpath('//div[@id="d_content"]/p/text()')
        end_right_content_num = len(root.xpath('//div[@id="d_content"]/p[@style="text-align: right;"]/text()'))
        main_content, end_content = '\n'.join(content[0:end_right_content_num * (-1)]), '\n'.join(content[end_right_content_num * (-1):])

        # print title, date, re.search(u'来源:(.+)',from_gov).groups(1)[0]
        # print total_content.strip()
        # print main_content, end_content

        # 数据库查重
        cur = db.cursor()
        sql = "select count(*) from news_gov_msg where url='%s'" % each_page_url
        cur.execute(sql)
        res = cur.fetchone()[0]
        if res:
            print title, 'has existed in the database.'
            cur.close()
        else:
            # 入库爬到的数据
            sql = "INSERT INTO news_gov_msg(title, url, msg_from, msg_date, whole_content, main_content, end_content, site_from) VALUES('%s','%s','%s','%s','%s','%s','%s','%s')" % (
            title, each_page_url, re.search(u'来源:(.+)',from_gov).groups(1)[0], date, total_content.strip(), main_content, end_content, u'成都高新区')
            cur.execute(sql)
            db.commit()
            cur.close()

        download_url_num = len(root.xpath('//*[starts-with(@id, "attach")]'))  # ！！！！！！！！！！！
        download_url_name = root.xpath('//*[starts-with(@id, "attach")]/text()')

        down_url = 'http://www.cdht.gov.cn/attachment_url.jspx?cid=%s&n=%d' %(cid, download_url_num)
        json_key = requests.get(down_url).json()
        for i in range(download_url_num):
            real_url = 'http://www.cdht.gov.cn/attachment.jspx?cid=%s&i=%d' % (cid, i) + json_key[i]
            # print real_url

            # 查重
            cur = db.cursor()
            sql = "select count(*) from news_file where file_name='%s' and from_url='%s'" % (download_url_name[i], each_page_url)
            cur.execute(sql)
            res = cur.fetchone()[0]
            if res:
                print download_url_name[i], 'has existed in the database.'
                cur.close()
                continue

            # 插文件信息入库
            sql = "INSERT INTO news_file(from_url, file_name, file_url) VALUES ('%s','%s','%s')" % (
            each_page_url, download_url_name[i], real_url)
            cur.execute(sql)
            db.commit()
            cur.close()
        # 通过selenium爬动态内容
        # from selenium import webdriver
        #
        # try:
        #     browser = webdriver.Chrome(executable_path='chromedriver.exe')
        #     browser.get(each_page_url)
        #     for i in range(download_url_num):
        #         download_url = browser.find_element_by_id('attach%d' % i).get_attribute('href')
        #         # print download_url_name[i], download_url
        #         cur = db.cursor()
        #
        #         # 查重
        #         sql = "select count(*) from news_file where file_url='%s'" % download_url
        #         cur.execute(sql)
        #         res = cur.fetchone()[0]
        #         if res:
        #             print download_url, 'has existed in the database.'
        #             cur.close()
        #             continue
        #
        #         # 插文件信息入库
        #         sql = "INSERT INTO news_file(from_url, file_name, file_url) VALUES ('%s','%s','%s')" % (each_page_url, download_url_name[i], download_url)
        #         cur.execute(sql)
        #         db.commit()
        #         cur.close()
        # finally:
        #     browser.quit()
    db.close()

if __name__ == '__main__':
    url = u'http://www.cdht.gov.cn/jbxxgk/index.jhtml?title=%E7%94%B3%E6%8A%A5'
    every_page_url = get_urls(url)
    # every_page_url = ['http://www.cdht.gov.cn/zwgktzgg/139755.jhtml']
    get_each_gov_msg(every_page_url)
