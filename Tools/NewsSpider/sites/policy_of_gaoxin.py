# coding:utf8
"""
--------------------------------------------------------------------------
    File:   policy_of_gaoxin.py
    Auth:   zsdostar
    Date:   2018/2/27 18:34
    Sys:    Windows 10
--------------------------------------------------------------------------
    Desc:   
--------------------------------------------------------------------------
"""
import requests
import re
import time
import pymysql

from lxml import etree

from company import COM, GOV


def get_urls(in_url):
    urls = []
    content = requests.get(in_url).content
    root = etree.HTML(content)

    # 获取该搜索结果的页数
    temp_text = root.xpath('//div[@class="text-center pagin mt20 pb20"]/div/text()')[0]
    index_num = int(re.search(u'/(\d+)页', temp_text).group(1))
    # 从每页获取每个标题的URL并存入urls中
    for i in range(1,index_num+1):
        thispage_url = in_url.replace('/index.jhtml', '/index_%d.jhtml' % i)
        content = requests.get(thispage_url).content
        root = etree.HTML(content)

        each_title_urls = root.xpath('//tbody/tr/td/a/@href')
        urls.extend(each_title_urls)
    return urls


def get_each_gov_msg(every_page_url):
    for each_page_url in every_page_url:
        content = requests.get(each_page_url).content
        root = etree.HTML(content)

        title = root.xpath('//div[@class="page"]/h1/text()')[0]
        date = root.xpath('//div[@class="sx col-md-6"]/span[1]/text()')[0]
        from_gov = root.xpath('//div[@class="sx col-md-6"]/span[2]/text()')[0]

        # 不清楚哪种存word比较好，故此都存下了，end_right_content_num是为了切割正文main_content和落款end_content的
        total_content = root.xpath('string(//div[@id="d_content"])')  # ！！！！！！！！！！！！！！！
        content = root.xpath('//div[@id="d_content"]/p/text()')
        end_right_content_num = len(root.xpath('//div[@id="d_content"]/p[@style="text-align: right;"]/text()'))
        main_content, end_content = content[0:end_right_content_num*(-1)], content[end_right_content_num*(-1):]

        download_url_num = len(root.xpath('//*[starts-with(@id, "attach")]'))  # ！！！！！！！！！！！
        download_url_name = root.xpath('//*[starts-with(@id, "attach")]/text()')

        # print title, date, from_gov
        # print total_content
        from selenium import webdriver


        browser = webdriver.Chrome(executable_path='chromedriver.exe')
        browser.get(each_page_url)
        time.sleep(2)
        download_url = browser.find_element_by_id('attach0').get_attribute('href')
        print download_url_name, download_url
        browser.quit()


if __name__ == '__main__':
    url = u'http://www.cdht.gov.cn/jbxxgk/index.jhtml?title=%E7%94%B3%E6%8A%A5'
    # every_page_url = get_urls(url)
    every_page_url = ['http://www.cdht.gov.cn/zwgktzgg/143370.jhtml']
    get_each_gov_msg(every_page_url)
