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

while True:
    DATE1 = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    DATE2 = time.strftime('%Y-%m-%d',time.localtime(time.time()))

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
    ofweek.DATE = DATE1
    ofweek.main()
    wulianchina.DATE = DATE2
    wulianchina.main()
    
    time.sleep(2*3600)
