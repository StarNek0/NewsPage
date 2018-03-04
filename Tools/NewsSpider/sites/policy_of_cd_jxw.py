# coding:utf8
"""
--------------------------------------------------------------------------
    File:   policy_of_cd_jxw.py
    Auth:   zsdostar
    Date:   2018/3/4 12:32
    Sys:    Windows 10
--------------------------------------------------------------------------
    Desc:   成都经信委项目申报爬虫
--------------------------------------------------------------------------
"""
import requests
import re
import time
import pymysql
import datetime

from lxml import etree

url = 'http://www.cdgy.gov.cn/newList1Level.jsp?classId=010501&firstNo=0105&num=null'

d={'classId':010501,'SearchWord':None,'p':3,'t':0,}
h = {
 'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
 'Cookie':'gwdshare_firstime=1520068960456; JSESSIONID=2C75B866B2F6C949795FDB534CF2EB65; _gscbrs_1405241782=1; _gscu_1405241782=20068960efrgjy55; Hm_lvt_61f86a9a2787e317b406b4d31819fd81=1520079527,1520079865,1520080678,1520137183; Hm_lpvt_61f86a9a2787e317b406b4d31819fd81=1520140155',
}
r = requests.post(url, data=d,headers=h)
print r.text