from django.db import models
from datetime import datetime
from users.models import MyMessage

# Create your models here.


class MajorSystem(models.Model):
    college = models.CharField(verbose_name='学院', max_length=50)
    major = models.CharField(verbose_name='专业', max_length=50)
    c_type = models.CharField(verbose_name='课程性质', max_length=100)
    sum_credit = models.FloatField(verbose_name='总学分', default=0)
    add_time = models.DateTimeField(verbose_name=u"添加时间", default=datetime.now)

    class Meta:
        verbose_name = '学分要求'
        verbose_name_plural = verbose_name
        get_latest_by = 'add_time'
        ordering = ['id']

    def __str__(self):
        return self.c_type


class Coursetable(models.Model):
    c_id = models.CharField(verbose_name='课程代码', max_length=30, null=False, unique=True)
    title = models.CharField(verbose_name='课程名', max_length=50)
    credit = models.FloatField(verbose_name='学分', default=0.0)
    period = models.CharField(verbose_name='学时', max_length=10)
    semester = models.CharField(verbose_name='开课学期', max_length=10)
    c_type = models.ForeignKey(MajorSystem,verbose_name='课程性质',on_delete=models.CASCADE)
    major = models.CharField(verbose_name='专业', max_length=50)
    college = models.CharField(verbose_name='学院', max_length=50)
    add_time = models.DateTimeField(verbose_name=u"添加时间", default=datetime.now)

    class Meta:
        verbose_name = '所有课程'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class StCredit(models.Model):
    st_id = models.CharField(verbose_name='学号', max_length=50, unique=True)
    name = models.CharField(verbose_name='姓名', max_length=50)
    accomplish = models.FloatField(verbose_name='已修学分',default=0)
    unfinshed = models.FloatField(verbose_name='未修学分', default=0)
    c_type = models.CharField(verbose_name='课程性质', max_length=100)
    add_time = models.DateTimeField(verbose_name=u"添加时间", default=datetime.now)

    class Meta:
        verbose_name = '学生学分管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class StGgrade(models.Model):
    st_id = models.CharField(verbose_name='学号', max_length=50)
    title = models.CharField(verbose_name='课程名', max_length=50)
    credit = models.FloatField(verbose_name='学分', default=0.0)
    grade = models.FloatField(verbose_name='成绩', default=0.0)
    year = models.CharField(verbose_name='学年', max_length=20)
    semester = models.CharField(verbose_name='学期', max_length=10)
    c_type = models.ForeignKey(MajorSystem,verbose_name='课程性质',on_delete=models.CASCADE)
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)

    class Meta:
        verbose_name = '历年成绩'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class LearnWarning(models.Model):
    st_id = models.ForeignKey('users.MyMessage', on_delete=models.CASCADE, verbose_name='学号', max_length=50)
    name = models.CharField(verbose_name='姓名',max_length=20)
    year = models.CharField(verbose_name='学年', max_length=20)
    semester = models.CharField(verbose_name='学期', max_length=10)
    college = models.CharField(verbose_name='学院', max_length=20, default='计算机学院')
    major = models.CharField(verbose_name='专业', max_length=20, default='')
    grade = models.CharField(verbose_name='年级', max_length=20)
    myclass = models.CharField(verbose_name='班级', max_length=10)
    is_send = models.IntegerField(verbose_name='发送短信',default=0)
    level = models.CharField(verbose_name='预警等级', choices=(('退学预警',"退学预警"),('降级预警',"降级预警"),('跟班修读','跟班修读'),('警示预警','警示预警')),max_length=10,  default='正常')
    warm_creadit = models.FloatField(verbose_name='挂科学分',default=0)
    message = models.TextField(verbose_name='预警消息',default='正常')
    assit_teacher = models.CharField(verbose_name='帮扶老师',max_length=30,default='')
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)

    class Meta:
        verbose_name = '预警消息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.level


class WarnRule(models.Model):
    school_name = models.CharField(verbose_name='学校名称', max_length=50, default='北方民族大学')
    level = models.CharField(verbose_name='预警等级', max_length=30)
    sum_credit = models.FloatField(verbose_name='一学年所需学分', default=0)
    all_credit = models.FloatField(verbose_name='在校期间所需学分', default=0)
    truant = models.IntegerField(verbose_name='旷课节数', null=True, blank=True)
    item = models.TextField(verbose_name='其他',null=True, blank=True)
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)

    class Meta:
        verbose_name = '预警等级'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.level