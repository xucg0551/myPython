from django.conf.urls import url, include
from django.views.static import serve
from django.views.generic import TemplateView
from django.conf import settings

import xadmin
from users.views import LoginView, IndexView, LogoutView, RegisterView, ActivateView
from xxonline.settings import MEDIA_ROOT

urlpatterns = [
    url(r'xadmin/', xadmin.site.urls),
    # url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^activate/(?P<activate_code>.*)/$', ActivateView.as_view(), name='activate'),

    #图片处理函数
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),

    #验证码处理函数
    url(r'^captcha/', include('captcha.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns.append(url(r'^__debug__/', include(debug_toolbar.urls)))

