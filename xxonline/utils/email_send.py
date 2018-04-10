import random
import string
from django.core.mail import send_mail

from users.models import EmailVerifyRecord
from django.conf import settings


def random_code(size, chars=string.ascii_letters+string.digits):
    return ''.join([random.choice(chars) for _ in range(size)])


def send_email(email, send_type="register"):
    code = random_code(16)
    EmailVerifyRecord.objects.update_or_create(email=email, send_type=send_type,
                                               defaults={'code': code, 'is_verified': False})
    ##以下方法等同于上面的update_or_create
    # try:
    #     record = EmailVerifyRecord.objects.get(email=email, send_type=send_type)
    #     if record:
    #         record.code = code
    #         record.is_verified = False
    #         record.save()
    # except EmailVerifyRecord.DoDoesNotExist:
    #     EmailVerifyRecord.objects.create(email=email, code=code, send_type=send_type)




    if send_type == "register":
        email_title = "cgonline 激活用户"
        email_body = "请点击下面的链接激活你的账号: http://127.0.0.1:8080/activate/{0}/{1}".format(code, email)

        send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])
    elif send_type == "forget":
        email_title = "cgonlie 重置登录密码"
        email_body = "请点击下面的链接重置登录密码: http://127.0.0.1:8080/reset/{0}/{1}".format(code, email)

        send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])
    elif send_type == "update_email":
        email_title = "慕学在线邮箱修改验证码"
        email_body = "你的邮箱验证码为: {0}".format(code)

        send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])
    return send_status
