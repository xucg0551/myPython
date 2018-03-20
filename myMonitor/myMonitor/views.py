#__author__ = ‘Shane‘
# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

def index(request):
    print(request.path)
    return HttpResponseRedirect(reverse('login', args=(1024,)))

def login(request, id):
    print(request.path)
    print(request.user)
    print(request.GET.urlencode)
    print(request.META)
    print(request.COOKIES)
    return HttpResponse(id)