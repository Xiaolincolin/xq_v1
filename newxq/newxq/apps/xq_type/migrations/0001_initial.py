# Generated by Django 2.2.2 on 2019-06-11 17:10

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Types',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(max_length=50, unique=True, verbose_name='类名')),
                ('desc', models.TextField(blank=True, null=True, verbose_name='描述')),
                ('click_times', models.IntegerField(default=0, verbose_name='点击次数')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '总分类',
                'verbose_name_plural': '总分类',
            },
        ),
        migrations.CreateModel(
            name='Technologys',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='技能名称')),
                ('note', models.CharField(max_length=300, verbose_name='描述')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('type_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='xq_type.Types')),
            ],
            options={
                'verbose_name': '涉及技能',
                'verbose_name_plural': '涉及技能',
            },
        ),
        migrations.CreateModel(
            name='personal_type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='姓名')),
                ('st_id', models.CharField(max_length=50, verbose_name='学号')),
                ('college', models.CharField(max_length=20, verbose_name='学院')),
                ('major', models.CharField(max_length=20, verbose_name='专业')),
                ('myclass', models.CharField(max_length=10, verbose_name='班级')),
                ('title', models.CharField(max_length=200, verbose_name='标题')),
                ('click_times', models.IntegerField(default=0, verbose_name='点击次数')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('type_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='xq_type.Types')),
            ],
            options={
                'verbose_name': '个人分类',
                'verbose_name_plural': '个人分类',
            },
        ),
    ]
