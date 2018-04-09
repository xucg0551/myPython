from django import forms

from captcha.fields import CaptchaField


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True, initial='')
    password = forms.CharField(required=True, min_length=5, initial='')
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'}, initial='')
