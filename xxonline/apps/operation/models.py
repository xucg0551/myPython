from django.db import models

from datetime import datetime


class UserMessage(models.Model):
    user = models.IntegerField(verbose_name=u"接收用户", default=0)
    message = models.CharField(verbose_name=u"消息内容", max_length=500)
    has_read = models.BooleanField(verbose_name=u"是否已读", default=False)
    add_time = models.DateTimeField(verbose_name=u"添加时间", default=datetime.now)

    class Meta:
        verbose_name = u"用户消息"
        verbose_name_plural = verbose_name
