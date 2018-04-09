from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.generic.base import View
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse

from users.forms import LoginForm
from users.models import Banner


class IndexView(View):
    def get(self, request):
        #获取轮播图
        all_banners = Banner.objects.all()
        return render(request, 'index.html', {
            'all_banners': all_banners
        })


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        #首先验证表单，再进行用户验证，最后登录
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=user_name, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
                # return render(request, 'index.html')
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误'})

        else:
            return render(request, 'login.html', {'login_form': login_form})
