#__author__ = ‘Shane‘
# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse


def cookie_test(request):
    response = HttpResponse('This is a cookie test')
    response.set_cookie('myMonitorId', '102478955')
    response.set_cookie('myMonitroId2', '212456666')
    return response