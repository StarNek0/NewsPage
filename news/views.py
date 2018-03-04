#coding:utf-8
import time
from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
from .models import news,GOV_MSG,FILE


def DtCalc(stTime, edTime):
    st = time.mktime(time.strptime(stTime, "%Y-%m-%d"))
    ed = edTime

    return int((ed - st) / (24 * 3600))  # 时间差/天

class NewsView(View):
    def get(self, request, date=None):
        if date is None:
            date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        DATE_Array = time.strptime(date, '%Y-%m-%d')
        DATE_Stamp = int(time.mktime(DATE_Array))
        front_date=time.strftime('%Y-%m-%d', time.localtime(DATE_Stamp-24*3600))
        behind_date=time.strftime('%Y-%m-%d', time.localtime(DATE_Stamp+24*3600))
        
        News_pages = news.objects.filter(page_date=date, tag=u'资讯').order_by('-score')
        Policy_pages = news.objects.filter(page_date=date, tag=u'政策').order_by('-score')
        Company_pages = news.objects.filter(page_date=date, tag=u'企业').order_by('-score')
        ChanYe_pages = news.objects.filter(page_date=date, tag=u'产业').order_by('-score')
        YingYong_pages = news.objects.filter(page_date=date, tag=u'应用').order_by('-score')

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


class ProjectView(View):

    def get(self, request):
        all_projects = GOV_MSG.objects.all()

        # hot_orgs = all_orgs.order_by('-click_num')[:3]


        # 搜索功能
        # search_keywords = request.GET.get('keywords', '')
        # if search_keywords:
        #     all_orgs = all_orgs.filter(
        #         Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords))  # i是不区分大小写

        # 城市筛选
        # city_id = request.GET.get('city', "")
        # if city_id:
        #     all_orgs = all_orgs.filter(city_id=int(city_id))

        # 机构类别筛选
        category = request.GET.get('ct', '')
        if category:
            all_projects = all_projects.filter(site_from=category)

        # sort = request.GET.get('sort', "")
        # if sort:
        #     if sort == "students":
        #         all_orgs = all_orgs.order_by('-students')
        #     elif sort == "courses":
        #         all_orgs = all_orgs.order_by('-course_nums')
        #
        # org_nums = all_orgs.count()  # 课程总数

        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_projects, 5, request=request)
        all_projects = p.page(page)

        return render(request, 'project-list.html', {
            'all_projects': all_projects,
            'category': category,
        })

