from django.contrib.auth.models import AbstractUser
from django.db import models

from datetime import datetime


class UserProfile(AbstractUser):
    #字段、Meta、__str__
    nick_name = models.CharField(verbose_name=u"昵称", max_length=50,  default="")
    birthday = models.DateField(verbose_name=u"生日", null=True, blank=True)
    gender = models.CharField(verbose_name=u'性别', max_length=6, choices=(("male", u"男"), ("female", "女")), default="female")
    address = models.CharField(verbose_name=u'地址', max_length=100, default=u"")
    mobile = models.CharField(verbose_name=u'电话', max_length=11, null=True, blank=True)
    image = models.ImageField(verbose_name=u'图片', upload_to="image/%Y/%m", default=u"image/default.png", max_length=100)

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
#
#     # def unread_nums(self):
#     #     #获取用户未读消息的数量
#     #     from operation.models import UserMessage
#     #     return UserMessage.objects.filter(user=self.id, has_read=False).count()


class Banner(models.Model):
    title = models.CharField(verbose_name=u"标题", max_length=100)
    image = models.ImageField(verbose_name=u"轮播图", upload_to="banner/%Y/%m", max_length=100)
    url = models.URLField(verbose_name=u"访问地址", max_length=200)
    index = models.IntegerField(verbose_name=u"顺序", default=100)
    add_time = models.DateTimeField(verbose_name=u"添加时间", default=datetime.now)

    class Meta:
        verbose_name = u"轮播图"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class EmailVerifyRecord(models.Model):
    code = models.CharField(verbose_name=u"验证码", max_length=20)
    email = models.EmailField(verbose_name=u"邮箱", max_length=50)
    send_type = models.CharField(verbose_name=u"验证码类型", choices=(("register", u"注册"), ("forget", u"找回密码"), ("update_email", u"修改邮箱")), max_length=30)
    send_time = models.DateTimeField(verbose_name=u"发送时间", default=datetime.now)
    is_verified = models.BooleanField(verbose_name=u'是否验证过', default=False)
    # expiration = models.DateTimeField(verbose_name=u"失效时间")

    class Meta:
        verbose_name = u"邮箱验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}({1})'.format(self.code, self.email)
