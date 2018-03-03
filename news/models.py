# coding:utf-8
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class news(models.Model):
    head = models.CharField(max_length=255, verbose_name="标题")
    theme = models.TextField(verbose_name="主题", null=True, blank=True)
    score = models.IntegerField(verbose_name='评分',default=0)
    content = models.TextField(verbose_name="全文", null=True, blank=True)
    source_site = models.CharField(max_length=255, verbose_name="来源站")
    source_url = models.CharField(max_length=255, verbose_name="来源URL")
    tag = models.CharField(max_length=255, verbose_name="标签")
    keywords = models.CharField(max_length=255, verbose_name="关键词")
    page_date = models.CharField(max_length=255, verbose_name="日期")
    class Meta:
        verbose_name='news'
        verbose_name_plural='news'
    def __unicode__(self):
        return self.theme

class GOV_MSG(models.Model):
    title = models.CharField(max_length=255, verbose_name="标题")
    url = models.CharField(max_length=255, verbose_name="URL", null=True)
    msg_from = models.CharField(max_length=255, verbose_name="来源单位", null=True)
    site_from = models.CharField(max_length=255, verbose_name="来源网站", null=True)
    msg_date = models.CharField(max_length=255, verbose_name="发布日期", null=True)
    msg_end_date = models.CharField(max_length=255, verbose_name="截止日期", null=True)
    whole_content = models.TextField(verbose_name="全文", null=True, blank=True)
    main_content = models.TextField(verbose_name="正文", null=True, blank=True)
    end_content = models.TextField(verbose_name="落款", null=True, blank=True)
    class Meta:
        verbose_name='gov'
        verbose_name_plural='gov'
    def __unicode__(self):
        return self.title


class FILE(models.Model):
    from_url = models.CharField(max_length=255, verbose_name="URL")
    file_name = models.CharField(max_length=255, verbose_name="标题")
    file_url = models.CharField(max_length=255, verbose_name="标题")
    class Meta:
        verbose_name='file'
        verbose_name_plural='file'
    def __unicode__(self):
        return self.file_name