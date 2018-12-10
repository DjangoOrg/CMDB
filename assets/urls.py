# !usr/bin/env python3
# encoding:utf-8
"""
@project = cmdb
@file = urls
@author = 'Easton Liu'
@creat_time = 2018/12/10 19:28
@explain:

"""
from django.urls import path
from assets import views
urlpatterns = [
    path('report/',views.report,name='report')
]