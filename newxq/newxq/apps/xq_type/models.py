from django.db import models
from datetime import datetime


class Types(models.Model):

    type_name = models.CharField(verbose_name='类名',max_length=50,unique=True)
    desc = models.TextField(verbose_name='描述',null=True, blank=True)
    click_times = models.IntegerField(verbose_name='点击次数',default=0)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    class Meta:
        verbose_name = '总分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.type_name


class personal_type(models.Model):
    name = models.CharField(verbose_name='姓名', max_length=50)
    st_id = models.CharField(verbose_name='学号', max_length=50)
    college = models.CharField(verbose_name='学院', max_length=20)
    major = models.CharField(verbose_name='专业', max_length=20)
    myclass = models.CharField(verbose_name='班级', max_length=10)
    title = models.CharField(verbose_name='标题',max_length=200,)
    type_name = models.ForeignKey('Types',on_delete=models.CASCADE)
    click_times = models.IntegerField(verbose_name='点击次数',default=0)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    class Meta:
        verbose_name = '个人分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.st_id

class Technologys(models.Model):
    type_name = models.ForeignKey('Types',on_delete=models.CASCADE)
    level = models.IntegerField(verbose_name='等级')
    percentage = models.IntegerField(verbose_name='未知')
    name = models.CharField(verbose_name='技能名称',max_length=50)
    note = models.CharField(verbose_name='描述',max_length=300)
    class Meta:
        verbose_name = '涉及技能'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
