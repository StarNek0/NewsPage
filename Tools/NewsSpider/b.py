# coding:utf8
"""
--------------------------------------------------------------------------
    File:   b.py
    Auth:   zsdostar
    Date:   2018/2/22 23:09
    Sys:    Windows 10
--------------------------------------------------------------------------
    Desc:   
--------------------------------------------------------------------------
"""
import time
date = '2018-02-22'

DATE_Array = time.strptime(date, '%Y-%m-%d')
DATE_Stamp = int(time.mktime(DATE_Array))
front_date=time.strftime('%Y-%m-%d', time.localtime(DATE_Stamp-24*3600))
behind_date=time.strftime('%Y-%m-%d', time.localtime(DATE_Stamp+24*3600))
print front_date, behind_date