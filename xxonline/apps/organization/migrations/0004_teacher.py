# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-04-12 00:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0003_auto_20180411_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='教师名')),
                ('work_years', models.IntegerField(default=0, verbose_name='工作年限')),
                ('work_company', models.CharField(max_length=50, verbose_name='就职公司')),
                ('work_position', models.CharField(max_length=50, verbose_name='公司职位')),
                ('points', models.CharField(max_length=50, verbose_name='教学特点')),
                ('click_nums', models.IntegerField(default=0, verbose_name='点击数')),
                ('fav_nums', models.IntegerField(default=0, verbose_name='收藏数')),
                ('age', models.IntegerField(default=18, verbose_name='年龄')),
                ('image', models.ImageField(default='', upload_to='teacher/%Y/%m', verbose_name='头像')),
                ('add_time', models.DateTimeField(auto_now=True)),
                ('org', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.CourseOrg', verbose_name='所属机构')),
            ],
            options={
                'verbose_name': '教师',
                'verbose_name_plural': '教师',
            },
        ),
    ]