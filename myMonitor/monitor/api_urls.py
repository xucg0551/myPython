#__author__ = ‘Shane‘
# -*- coding: utf-8 -*-

from django.conf.urls import url

from  monitor import views

urlpatterns = [
    url(r'client/config/(\d+)/$', views.client_configs),
]
