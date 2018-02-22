# coding:utf-8
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class news(models.Model):
    head = models.CharField(max_length=255, verbose_name="标题")
    theme = models.TextField(verbose_name="主题", null=True, blank=True)
    content = models.TextField(verbose_name="全文", null=True, blank=True)
    source_site = models.CharField(max_length=255, verbose_name="来源站")
    source_url = models.CharField(max_length=255, verbose_name="来源URL")
    tag = models.CharField(max_length=255, verbose_name="标签")
    keywords = models.CharField(max_length=255, verbose_name="关键词")
    page_date = models.CharField(max_length=255, verbose_name="日期")