# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-04-11 23:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0002_userask'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userask',
            name='add_time',
            field=models.DateTimeField(auto_now=True, verbose_name='添加时间'),
        ),
    ]
