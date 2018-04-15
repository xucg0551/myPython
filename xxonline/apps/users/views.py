from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.core.urlresolvers import reverse
from django.contrib.auth.hashers import make_password
from django.db.models import Q

from users.forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm, UploadImageForm, UserInfoForm
from users.models import Banner, UserProfile, EmailVerifyRecord
from operation.models import UserMessage, UserCourse, UserFavorite
from courses.models import CourseOrg, Teacher, Course
from utils.email_send import send_email
from utils.mixin_utils import LoginRequiredMixin
from pure_pagination import PageNotAnInteger, Paginator
import json

class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
            else:
                return None
        except Exception as e:
            return None

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
            #判断邮箱是否注册过
            if UserProfile.objects.filter(email=user_name):
                return render(request, "register.html", {"register_form": register_form, "msg": "用户已经存在"})

            password = request.POST.get('password', '')
            user_profile = UserProfile()
            user_profile.email = user_name
            user_profile.username = user_name
            user_profile.is_active = False
            user_profile.password = make_password(password)
            user_profile.save()

            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = u'欢迎来到东莫村'
            user_message.save()

            #发送邮件用以激活
            send_status = send_email(user_name, 'register')
            if send_status == 1:
                return render(request, 'login.html')
            else:
                return render(request, "register.html", {"register_form": register_form, "msg": "发送邮件失败"})
        else:
            return render(request, 'register.html', {'register_form': register_form})


#激活用户
class ActivateView(View):
    def get(self, request, activate_code, email):
        # ev_record = EmailVerifyRecord.objects.filter(code=activate_code, email=email, is_verified=False)
        try:
            email_verify_record = EmailVerifyRecord.objects.get(code=activate_code, email=email, is_verified=False, send_type='register')
            if email_verify_record:
                email_verify_record.is_verified = True
                email_verify_record.save()

                user_profile = UserProfile.objects.get(email=email)
                user_profile.is_active = True
                user_profile.save()
                return render(request, 'login.html')
        except EmailVerifyRecord.DoesNotExist:
            return render(request, 'verify_code_fail.html')


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            account = request.POST.get('email', '')
            send_status = send_email(account, 'forget')
            if send_status == 1:
                return render(request, 'send_success.html')
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class ResetPwdView(View):
    def get(self, request, reset_code, email):
        try:
            email_verify_record = EmailVerifyRecord.objects.get(code=reset_code, email=email, is_verified=False, send_type='forget')
            if email_verify_record:
                email_verify_record.is_verified = True
                email_verify_record.save()
                return render(request, 'password_reset.html', {'email': email})
        except EmailVerifyRecord.DoesNotExist:
            return render(request, 'verify_code_fail.html')


class ModifyPwdView(View):
    def post(self, request):
        modify_pwd_form = ModifyPwdForm(request.POST)
        if modify_pwd_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {"email": email, "msg": "密码不一致"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()
            return render(request, "login.html")
        else:
            email = request.POST.get("email", "")
            return render(request, "password_reset.html", {"email": email, "modify_form": modify_pwd_form})

class UserinfoView(LoginRequiredMixin, View):
    """
    用户个人信息
    """
    def get(self, request):
        return render(request, 'usercenter-info.html', {})

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')

class UploadImageView(LoginRequiredMixin, View):
    """
    用户修改头像
    """
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')

class UpdatePwdView(View):
    """
    个人中心修改用户密码
    """
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}', content_type='application/json')
            user = request.user
            user.password = make_password(pwd2)
            user.save()

            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')

class SendEmailCodeView(LoginRequiredMixin, View):
    """
    发送邮箱验证码
    """
    def get(self, request):
        email = request.GET.get('email', '')

        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已经存在"}', content_type='application/json')
        send_email(email, "update_email")

        return HttpResponse('{"status":"success"}', content_type='application/json')

class UpdateEmailView(LoginRequiredMixin, View):
    """
    修改个人邮箱
    """
    def post(self, request):
        email = request.POST.get('email', '')
        update_code = request.POST.get('code', '')
        try:
            email_verify_record = EmailVerifyRecord.objects.get(code=update_code, email=email, is_verified=False, send_type='update_email')
            if email_verify_record:
                email_verify_record.is_verified = True
                email_verify_record.save()
                user = request.user
                user.email = email
                user.save()
                return HttpResponse('{"status":"success"}', content_type='application/json')
        except EmailVerifyRecord.DoesNotExist:
            return HttpResponse('{"email":"验证码出错"}', content_type='application/json')

class MyCourseView(LoginRequiredMixin, View):
    """
    我的课程
    """
    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html', {
            "user_courses":user_courses
        })

class MyFavOrgView(LoginRequiredMixin, View):
    """
    我收藏的课程机构
    """
    def get(self, request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)
        return render(request, 'usercenter-fav-org.html', {
            "org_list":org_list
        })


class MyFavTeacherView(LoginRequiredMixin, View):
    """
    我收藏的授课讲师
    """
    def get(self, request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)
        return render(request, 'usercenter-fav-teacher.html', {
            "teacher_list":teacher_list
        })


class MyFavCourseView(LoginRequiredMixin, View):
    """
    我收藏的课程
    """
    def get(self, request):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            teacher = Course.objects.get(id=course_id)
            course_list.append(teacher)
        return render(request, 'usercenter-fav-course.html', {
            "course_list":course_list
        })

class MymessageView(LoginRequiredMixin, View):
    """
    我的消息
    """
    def get(self, request):
        all_messages = UserMessage.objects.filter(user=request.user.id)

        #用户进入个人消息后清空未读消息的记录
        all_unread_messages = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for unread_message in all_unread_messages:
            unread_message.has_read = True
            unread_message.save()

        #对个人消息进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_messages, 5, request=request)

        messages = p.page(page)
        return render(request, 'usercenter-message.html', {
            "messages":messages,
            'current_page':'my_message'
        })



