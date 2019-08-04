from django.db import models
from xq_type.models import Types
from datetime import datetime


# Create your models here.
class Artcle(models.Model):
    title = models.CharField(verbose_name='资讯名', max_length=50, default='')
    url = models.URLField(verbose_name='链接地址', max_length=200, default='')
    content = models.TextField(verbose_name='正文', default='')
    type_name = models.ForeignKey(Types,verbose_name='标签',on_delete=models.CASCADE)
    click_times = models.IntegerField(verbose_name='点击次数',default=0)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = '热门资讯'
        verbose_name_plural = verbose_name
        get_latest_by = 'add_time'
        ordering = ['id']

    def __str__(self):
        return self.title


class HotJob(models.Model):
    title = models.CharField(verbose_name='职位名', max_length=50)
    salary = models.CharField(verbose_name='薪资', max_length=30, default='')
    url = models.URLField(verbose_name='链接地址', max_length=200, default='')
    content = models.TextField(verbose_name='正文', null=True, blank=True)
    type_name = models.ForeignKey(Types,verbose_name='标签',on_delete=models.CASCADE)
    click_times = models.PositiveIntegerField(verbose_name='点击次数',default=0)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = '热门职位'
        verbose_name_plural = verbose_name
        get_latest_by = 'add_time'
        ordering = ['id']

    def viewed(self):
        self.click_times += 1
        self.save(update_fields=['click_times'])

    def __str__(self):
        return self.title


class HotProject(models.Model):
    title = models.CharField(verbose_name='项目名', max_length=50, default='')
    url = models.URLField(verbose_name='地址', max_length=200, default='')
    type_name = models.ForeignKey(Types,verbose_name='标签',on_delete=models.CASCADE)
    click_times = models.IntegerField(verbose_name='点击次数',default=0)
    content = models.TextField(verbose_name='正文', null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = '最热开源项目'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class BorrowBook(models.Model):
    st_id = models.CharField(verbose_name='学号',max_length=50,default='')
    title = models.CharField(verbose_name='书名', max_length=100, default='')
    type_name = models.ForeignKey(Types, verbose_name='标签',on_delete=models.CASCADE)
    borrow_times = models.IntegerField(verbose_name='借阅次数',default=0)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = '图书馆借书'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Banner(models.Model):
    title = models.CharField(verbose_name='大赛名', max_length=200, default='')
    type_name = models.ForeignKey(Types,verbose_name='标签',on_delete=models.CASCADE)
    url = models.URLField(verbose_name='链接地址', max_length=200, default='')
    content = models.TextField(verbose_name="简介", null=True, blank=True)
    image = models.ImageField(upload_to="banner/%Y/%m",default="banner/default.png", verbose_name=u"轮播图", max_length=100)
    index = models.IntegerField(default=100, verbose_name=u"顺序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = '大赛信息'
        verbose_name_plural = verbose_name


    def __str__(self):
        return self.title