from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url('^$', views.cookie_test),
    url('^api/', include('monitor.api_urls'))   #关于接口api/ 的请求都分发给api_urls处理
]
