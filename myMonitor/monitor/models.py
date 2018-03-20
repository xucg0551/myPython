from django.db import models

# Create your models here.

class Host(models.Model):
    name = models.CharField(max_length=64, unique=True)
    ip_addr = models.GenericIPAddressField(u'IP地址',unique=True)
    monitored_by_choices = (
        ('agent', 'Agent'),
        ('snmp', 'SNMP'),
        ('wget', 'WGET')
    )
    monitored_by = models.CharField(u'监控方式', max_length=64, choices=monitored_by_choices)
    status_choices = (
        (1, 'Online'),
        (2, 'Down'),
        (3, 'Unreachable'),
        (4, 'Offline'),
        (5, 'Problem')
    )
    host_alive_check_interval = models.IntegerField(u'主机存活状态检测间隔', default=30)
    status = models.IntegerField(u'状态', choices=status_choices, default=1)
    memo = models.TextField(u'备注', blank=True, null=True)

    def __str__(self):
        return self.name
