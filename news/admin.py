from django.contrib import admin

# Register your models here.
from .models import news,GOV_MSG,FILE
admin.site.register(news)
admin.site.register(GOV_MSG)
admin.site.register(FILE)