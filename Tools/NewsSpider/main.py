# coding:utf8
"""
--------------------------------------------------------------------------
    File:   main.py
    Auth:   zsdostar
    Date:   2018/2/13 17:42
    Sys:    Windows 10
--------------------------------------------------------------------------
    Desc:   
--------------------------------------------------------------------------
"""
import time

import sites.ofweek as ofweek
import sites.wulianchina as wulianchina

DATE = time.strftime('%Y-%m-%d',time.localtime(time.time()))
DATE = '2018-02-22'
print DATE
# i=0
# while True:
#     DATE = time.strftime('%Y-%m-%d',time.localtime(time.time()-i*(3600*24)))
#     i += 1
#     print DATE
#
#     ofweek.DATE = DATE
#     ofweek.main()
#
#     wulianchina.DATE = DATE
#     wulianchina.main()
ofweek.DATE = DATE
ofweek.main()
wulianchina.DATE = DATE
wulianchina.main()