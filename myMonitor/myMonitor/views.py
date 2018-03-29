#__author__ = ‘Shane‘
# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt


def cookie_test(request):
    print(request.META)
    response = HttpResponse('This is a cookie test')
    response.set_cookie('myMonitorId', '102478955')
    response.set_cookie('myMonitroId2', '212456666')
    return response

def session_test(request):
    print(request.COOKIES)
    if request.COOKIES:
       return HttpResponse('This test has cookies')
    else:
        return HttpResponse('This test has no cookies')
    return HttpResponse('This is a session test')

@csrf_exempt
def file_test(request):
    if request.method == 'POST':
        myFile = request.FILES.get('file', None)
        if not myFile:
            return HttpResponse('no files for upload')
        with open('{}'.format(myFile.name), 'wb') as f:
            for chunk in myFile.chunks():
                f.write(chunk)
    return HttpResponse('This is a file test')