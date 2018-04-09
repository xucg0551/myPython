"""xxonline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.views.static import serve

import xadmin
from users.views import LoginView, IndexView
from xxonline.settings import MEDIA_ROOT

###首页index.html 进入个人中心、我的消息、退出、注册、授课教师、授课机构、查看更多课程

urlpatterns = [
    url(r'xadmin/', xadmin.site.urls),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^login/$', LoginView.as_view(), name='login'),

    #图片处理函数
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT})
]

