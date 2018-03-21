from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible
class Host(models.Model):
    name = models.CharField(u'名称', max_length=64, unique=True)
    ip_addr = models.GenericIPAddressField(u'IP地址', unique=True)
    host_groups = models.ManyToManyField('HostGroup', blank=True)  #一台主机可以属于多个主机群，一个主机群也可以有多台主机
    templates = models.ManyToManyField('Template', blank=True)   #一台主机可以有多套模板，一套模板也可以对应多台主机
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

@python_2_unicode_compatible
class HostGroup(models.Model):
    name = models.CharField(u'名称', max_length=64, unique=True)
    templates = models.ManyToManyField('Template', blank=True)   #一个主机群可以有多套模板，一个模板也可以被多个主机群拥有
    memo = models.TextField(u'备注', blank=True, null=True)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class ServiceIndex(models.Model):   #监控指标
    name = models.CharField(max_length=64, unique=True)
    key = models.CharField(max_length=64)
    data_type_choices = (
        ('int', "int"),
        ('float', "float"),
        ('str', "string")
    )
    data_type = models.CharField(u'指标数据类型', max_length=32, choices=data_type_choices, default='init')
    memo = models.CharField(u'备注', max_length=128, blank=True, null=True)

    def __str__(self):
        return '{}.{}'.format(self.name, self.key)

@python_2_unicode_compatible
class Service(models.Model):
    name = models.CharField(u'服务名称', max_length=64, unique=True)
    interval = models.IntegerField(u'监控间隔', default=60)
    plugin_name = models.CharField(u'插件名', max_length=64, default='n/a')
    items = models.ManyToManyField('ServiceIndex', verbose_name=u'指标列表', blank=True)  #一个服务有多个监控指标，一个指标也可以属于多个服务
    has_sub_service = models.BooleanField(u'是否有子服务',default=False, help_text=u'如果一个服务还有独立的子服务 ,选择这个,比如 网卡服务有多个独立的子网卡')
    memo = models.CharField(u'备注', max_length=128, blank=True, null=True)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Template(models.Model):
    name = models.CharField(u'模板名称', max_length=64, unique=True)
    services = models.ManyToManyField('Service', verbose_name=u'服务列表')  #一个模板对应多个服务，一个服务也可以对应多个模板

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class TriggerExpression(models.Model):
    trigger = models.ForeignKey('Trigger', verbose_name=u"所属触发器", on_delete=models.CASCADE)
    service = models.ForeignKey(Service, verbose_name=u"关联服务", on_delete=models.CASCADE)
    service_index = models.ForeignKey(ServiceIndex, verbose_name=u"关联服务指标", on_delete=models.CASCADE)
    specified_index_key = models.CharField(verbose_name=u"只监控专门指定的指标key", max_length=64, blank=True, null=True)
    operator_type_choices = (('eq', '='), ('lt', '<'), ('gt', '>'))
    operator_type = models.CharField(u"运算符", choices=operator_type_choices, max_length=32)
    data_calc_type_choices = (
        ('avg', 'Average'),
        ('max', 'Max'),
        ('hit', 'Hit'),
        ('last', 'Last'),
    )
    data_calc_func = models.CharField(u"数据处理方式", choices=data_calc_type_choices, max_length=64)
    data_calc_args = models.CharField(u"函数传入参数", help_text=u"若是多个参数,则用,号分开,第一个值是时间", max_length=64)
    threshold = models.IntegerField(u"阈值")
    logic_type_choices = (('or', 'OR'), ('and', 'AND'))
    logic_type = models.CharField(u"与一个条件的逻辑关系", choices=logic_type_choices, max_length=32, blank=True, null=True)

    def __str__(self):
        return "%s %s(%s(%s))" % (self.service_index, self.operator_type, self.data_calc_func, self.data_calc_args)

@python_2_unicode_compatible
class Trigger(models.Model):
    name = models.CharField(u'角发器名称', max_length=64)
    severity_choices = (
        (1, 'Information'),
        (2, 'Warning'),
        (3, 'Average'),
        (4, 'High'),
        (5, 'Disaster'),
    )
    severity = models.IntegerField(u'警告级别', choices=severity_choices)
    enabled = models.BooleanField(default=True)
    memo = models.TextField(u'备注', blank=True, null=True)

    def __str__(self):
        return "<serice:%s, severity:%s>" %(self.name,self.get_severity_display())


@python_2_unicode_compatible
class Action(models.Model):
    '''定义trigger发生后，如何报警'''
    name = models.CharField(u'名称', max_length=64, unique=True)
    host_groups = models.ManyToManyField('HostGroup', blank=True)
    hosts = models.ManyToManyField('Host', blank=True)
    #........
    interval = models.IntegerField(u'告警间隔', default=300)
    operations = models.ManyToManyField('ActionOperation')
    recover_notice = models.BooleanField(u'故障恢复后发送通知消息', default=True)
    recover_subject = models.CharField(max_length=128, blank=True, null=True)
    recover_message = models.TextField(blank=True, null=True)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.name



@python_2_unicode_compatible
class ActionOperation(models.Model):
    '''报警动作列表'''
    name = models.CharField(u'名称', max_length=64)
    step = models.SmallIntegerField(u'第n次告警', default=1, help_text='当trigger触发次数小于这个值时就执行这条记录里报警方式')
    action_type_choices = (
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('script', 'RunScript'),
    )
    action_type = models.CharField(u'动作类型', choices=action_type_choices, default='email', max_length=64)
    #............
    _msg_format = 'Host({hostname}, {ip}) service({service_name}) has issue, msg:{msg}'
    msg_format = models.TextField(u'消息格式', default=_msg_format)

    def __str__(self):
        return self.name

# @python_2_unicode_compatible
# class UserProfile（