from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.hashers import make_password

from users.forms import LoginForm, RegisterForm
from users.models import Banner, UserProfile


#首页
class IndexView(View):
    def get(self, request):
        #获取轮播图
        all_banners = Banner.objects.all()
        return render(request, 'index.html', {
            'all_banners': all_banners
        })


#登录
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
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                    # return render(request, 'index.html')
                else:
                    return render(request, 'login.html', {'msg': '用户未激活'})
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误'})

        else:
            return render(request, 'login.html', {'login_form': login_form})


#退出
class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


#注册
class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email', '')
            if UserProfile.objects.filter(email=user_name):
                return render(request, "register.html", {"register_form": register_form, "msg": "用户已经存在"})
            password = request.POST.get('password', '')
            user_profile = UserProfile()
            user_profile.email = user_name
            user_profile.username = user_name
            user_profile.is_active = False
            user_profile.password = make_password(password)
            user_profile.save()

            return render(request, 'login.html')


        else:
            return render(request, 'register.html', {'register_form': register_form})

