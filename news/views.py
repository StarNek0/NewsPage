#coding:utf-8
import time
from django.shortcuts import render
from django.views.generic.base import View
# Create your views here.
from .models import news


class NewsView(View):
    def get(self, request, date=None):
        if date is None:
	    date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        DATE_Array = time.strptime(date, '%Y-%m-%d')
        DATE_Stamp = int(time.mktime(DATE_Array))
        front_date=time.strftime('%Y-%m-%d', time.localtime(DATE_Stamp-24*3600))
        behind_date=time.strftime('%Y-%m-%d', time.localtime(DATE_Stamp+24*3600))
        
        News_pages = news.objects.filter(page_date=date, tag=u'资讯')
        Policy_pages = news.objects.filter(page_date=date, tag=u'政策')
        Company_pages = news.objects.filter(page_date=date, tag=u'企业')
        ChanYe_pages = news.objects.filter(page_date=date, tag=u'产业')
        YingYong_pages = news.objects.filter(page_date=date, tag=u'应用')

        return render(request, 'index.html', {
            'News_pages':News_pages,
            'Policy_pages':Policy_pages,
            'Company_pages':Company_pages,
            'ChanYe_pages':ChanYe_pages,
            'YingYong_pages':YingYong_pages,

            'date': date,
            'format_date': date[5:],

            'front_date':front_date,
            'behind_date':behind_date,
        })
