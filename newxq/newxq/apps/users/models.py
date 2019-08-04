from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    colleage = models.CharField(verbose_name='学院',max_length=40,default='计算机学院')
    is_admin = models.CharField(verbose_name='身份',choices=(("stu","学生"),("admin","管理员")), max_length=6)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = '添加用户'
        verbose_name_plural = verbose_name


class MyMessage(models.Model):
    name = models.CharField(verbose_name='姓名', max_length=50)
    st_id = models.CharField(verbose_name='学号', max_length=50,unique=True)
    college = models.CharField(verbose_name='学院', max_length=20, default='')
    major = models.CharField(verbose_name='专业', max_length=20, default='')
    grade = models.CharField(verbose_name='年级', max_length=20,default='')
    myclass = models.CharField(verbose_name='班级',max_length=10,default='')
    phone_num = models.CharField(verbose_name='电话',max_length=11,null=True,blank=True)
    gender = models.CharField(max_length=6, choices=((u"male", "男"), ("famale", "女")), default="男")
    image = models.ImageField(verbose_name='头像', upload_to='my_info/%Y/%m', default='my_info/default.png',max_length=100)
    favor = models.TextField(verbose_name='专业兴趣', max_length=50, null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = '个人中心'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.st_id


class AssitStudy(models.Model):
    number = models.CharField(primary_key=True,verbose_name='学号', max_length=30)
    password = models.CharField(verbose_name='密码', max_length=50)
    name = models.CharField(verbose_name='姓名', max_length=30)
    rangeCode = models.CharField(verbose_name='随机码', max_length=30,default='')
    major = models.CharField(verbose_name='班级', max_length=30)
    grade = models.CharField(verbose_name='年级', max_length=30)
    job = models.CharField(verbose_name='姓名', max_length=30,null=True,blank=True)
    class Meta:
        verbose_name = '导向式助学'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.number

