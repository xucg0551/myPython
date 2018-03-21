# Generated by Django 2.0.2 on 2018-03-21 06:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='名称')),
                ('interval', models.IntegerField(default=300, verbose_name='告警间隔')),
                ('recover_notice', models.BooleanField(default=True, verbose_name='故障恢复后发送通知消息')),
                ('recover_subject', models.CharField(blank=True, max_length=128, null=True)),
                ('recover_message', models.TextField(blank=True, null=True)),
                ('enabled', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ActionOperation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='名称')),
                ('step', models.SmallIntegerField(default=1, help_text='当trigger触发次数小于这个值时就执行这条记录里报警方式', verbose_name='第n次告警')),
                ('action_type', models.CharField(choices=[('email', 'Email'), ('sms', 'SMS'), ('script', 'RunScript')], default='email', max_length=64, verbose_name='动作类型')),
                ('msg_format', models.TextField(default='Host({hostname}, {ip}) service({service_name}) has issue, msg:{msg}', verbose_name='消息格式')),
            ],
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='名称')),
                ('ip_addr', models.GenericIPAddressField(unique=True, verbose_name='IP地址')),
                ('monitored_by', models.CharField(choices=[('agent', 'Agent'), ('snmp', 'SNMP'), ('wget', 'WGET')], max_length=64, verbose_name='监控方式')),
                ('host_alive_check_interval', models.IntegerField(default=30, verbose_name='主机存活状态检测间隔')),
                ('status', models.IntegerField(choices=[(1, 'Online'), (2, 'Down'), (3, 'Unreachable'), (4, 'Offline'), (5, 'Problem')], default=1, verbose_name='状态')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='备注')),
            ],
        ),
        migrations.CreateModel(
            name='HostGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='名称')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='备注')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='服务名称')),
                ('interval', models.IntegerField(default=60, verbose_name='监控间隔')),
                ('plugin_name', models.CharField(default='n/a', max_length=64, verbose_name='插件名')),
                ('has_sub_service', models.BooleanField(default=False, help_text='如果一个服务还有独立的子服务 ,选择这个,比如 网卡服务有多个独立的子网卡', verbose_name='是否有子服务')),
                ('memo', models.CharField(blank=True, max_length=128, null=True, verbose_name='备注')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceIndex',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('key', models.CharField(max_length=64)),
                ('data_type', models.CharField(choices=[('int', 'int'), ('float', 'float'), ('str', 'string')], default='init', max_length=32, verbose_name='指标数据类型')),
                ('memo', models.CharField(blank=True, max_length=128, null=True, verbose_name='备注')),
            ],
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='模板名称')),
                ('services', models.ManyToManyField(to='monitor.Service', verbose_name='服务列表')),
            ],
        ),
        migrations.CreateModel(
            name='Trigger',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='角发器名称')),
                ('severity', models.IntegerField(choices=[(1, 'Information'), (2, 'Warning'), (3, 'Average'), (4, 'High'), (5, 'Disaster')], verbose_name='警告级别')),
                ('enabled', models.BooleanField(default=True)),
                ('memo', models.TextField(blank=True, null=True, verbose_name='备注')),
            ],
        ),
        migrations.CreateModel(
            name='TriggerExpression',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('specified_index_key', models.CharField(blank=True, max_length=64, null=True, verbose_name='只监控专门指定的指标key')),
                ('operator_type', models.CharField(choices=[('eq', '='), ('lt', '<'), ('gt', '>')], max_length=32, verbose_name='运算符')),
                ('data_calc_func', models.CharField(choices=[('avg', 'Average'), ('max', 'Max'), ('hit', 'Hit'), ('last', 'Last')], max_length=64, verbose_name='数据处理方式')),
                ('data_calc_args', models.CharField(help_text='若是多个参数,则用,号分开,第一个值是时间', max_length=64, verbose_name='函数传入参数')),
                ('threshold', models.IntegerField(verbose_name='阈值')),
                ('logic_type', models.CharField(blank=True, choices=[('or', 'OR'), ('and', 'AND')], max_length=32, null=True, verbose_name='与一个条件的逻辑关系')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitor.Service', verbose_name='关联服务')),
                ('service_index', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitor.ServiceIndex', verbose_name='关联服务指标')),
                ('trigger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitor.Trigger', verbose_name='所属触发器')),
            ],
        ),
        migrations.AddField(
            model_name='service',
            name='items',
            field=models.ManyToManyField(blank=True, to='monitor.ServiceIndex', verbose_name='指标列表'),
        ),
        migrations.AddField(
            model_name='hostgroup',
            name='templates',
            field=models.ManyToManyField(blank=True, to='monitor.Template'),
        ),
        migrations.AddField(
            model_name='host',
            name='host_groups',
            field=models.ManyToManyField(blank=True, to='monitor.HostGroup'),
        ),
        migrations.AddField(
            model_name='host',
            name='templates',
            field=models.ManyToManyField(blank=True, to='monitor.Template'),
        ),
        migrations.AddField(
            model_name='action',
            name='host_groups',
            field=models.ManyToManyField(blank=True, to='monitor.HostGroup'),
        ),
        migrations.AddField(
            model_name='action',
            name='hosts',
            field=models.ManyToManyField(blank=True, to='monitor.Host'),
        ),
        migrations.AddField(
            model_name='action',
            name='operations',
            field=models.ManyToManyField(to='monitor.ActionOperation'),
        ),
    ]
