from datetime import datetime

from django.db import models


# Create your models here.
class GraduateCheck(models.Model):
    name = models.CharField(verbose_name='姓名',max_length=30)
    st_id = models.CharField(verbose_name='学号', max_length=50)
    major = models.CharField(verbose_name='专业', max_length=20, default='')
    myclass = models.CharField(verbose_name='班级', max_length=10)
    sum_credit = models.FloatField(verbose_name='总学分', default=0)
    finish_credit = models.FloatField(verbose_name='已修学分', default=0)
    need_credit = models.FloatField(verbose_name='还需学分',default=0)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = '毕业审核'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.st_id


class StudenCreditManage(models.Model):
    name = models.CharField(verbose_name='姓名',max_length=30)
    st_id = models.CharField(verbose_name='学号', max_length=50)
    major = models.CharField(verbose_name='专业', max_length=20, default='')
    myclass = models.CharField(verbose_name='班级', max_length=10)
    sum_credit = models.FloatField(verbose_name='总学分', default=0)
    finish_credit = models.FloatField(verbose_name='已修学分', default=0)
    need_credit = models.FloatField(verbose_name='还需学分',default=0)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = '学分管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.st_id


class Assist(models.Model):
    name = models.CharField(verbose_name='姓名',max_length=30)
    st_id = models.CharField(verbose_name='学号', max_length=50)
    major = models.CharField(verbose_name='专业', max_length=20, default='')
    myclass = models.CharField(verbose_name='班级', max_length=10)
    warm_leve = models.CharField(verbose_name='预警等级', max_length=20,default='')
    assist_teacher = models.CharField(verbose_name='帮扶老师', max_length=20, default='', null=True,blank=True)
    job_number = models.ForeignKey('AssistTeacher',verbose_name='工号',on_delete=models.CASCADE)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = '帮扶计划'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.st_id


class AssistTeacher(models.Model):
    name = models.CharField(verbose_name='姓名',max_length=30)
    job_number = models.CharField(verbose_name='工号', max_length=50)
    phone = models.CharField(verbose_name='电话',max_length=11)
    college = models.CharField(verbose_name='学院', max_length=20, default='')
    major = models.CharField(verbose_name='专业', max_length=20, default='')
    assist_address = models.CharField(verbose_name='帮扶地点',max_length=100,null=True,blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '帮扶老师信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.job_number


class Assiot(models.Model):
    collage = models.CharField(verbose_name='学院',max_length=30)
    gender = models.CharField(max_length=6, choices=((u"male", "男"), ("famale", "女")), default="男")
    minzu = models.CharField(verbose_name='民族',max_length=30)
    jiguan = models.CharField(verbose_name='籍贯', max_length=30)
    major = models.CharField(verbose_name='专业', max_length=30)
    class Meta:
        verbose_name = '统计分析'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.collage


class AssociateBook(models.Model):
    student_id = models.CharField(verbose_name='学号', max_length=30)
    number = models.IntegerField(verbose_name='借阅次数')

    class Meta:
        verbose_name = '关联分析-借阅次数'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.student_id


class AssociateGrade(models.Model):
    student_id = models.CharField(verbose_name='学号', max_length=30)
    grade = models.IntegerField(verbose_name='成绩')

    class Meta:
        verbose_name = '关联分析-成绩'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.student_id


class BorrowAssociate(models.Model):
    student_id = models.CharField(verbose_name='学号', max_length=30)
    frequency = models.IntegerField(verbose_name='科目数')
    number = models.IntegerField(verbose_name='借阅次数')

    class Meta:
        verbose_name = '关联分析-借阅结果'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.student_id


class Associateaward(models.Model):
    student_id = models.CharField(verbose_name='学号', max_length=30)

    class Meta:
        verbose_name = '关联分析-奖励'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.student_id


class Associate_native_place(models.Model):
    student_id = models.CharField(verbose_name='学号', max_length=30)
    jiguan = models.CharField(verbose_name='籍贯', max_length=30)

    class Meta:
        verbose_name = '关联分析-籍贯'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.student_id


class AssociateGender(models.Model):
    student_id = models.CharField(verbose_name='学号', max_length=30)
    gender = models.CharField(max_length=6, choices=((u"male", "男"), ("famale", "女")), default="男")
    collage = models.CharField(verbose_name='学院', max_length=30)
    class Meta:
        verbose_name = '关联分析-学院男女'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.student_id


class AssociateCourseGrade(models.Model):
    student_id = models.CharField(verbose_name='学号', max_length=30)
    course_id = models.CharField(verbose_name='课程号', max_length=30)
    grade = models.IntegerField(verbose_name='成绩')
    class Meta:
        verbose_name = '关联分析-课程成绩'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.student_id


class AssociateCourse(models.Model):
    course_id = models.CharField(verbose_name='课程号', max_length=30)
    course_name = models.CharField(verbose_name='成绩', max_length=30)
    class Meta:
        verbose_name = '关联分析-课程成绩'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.course_id