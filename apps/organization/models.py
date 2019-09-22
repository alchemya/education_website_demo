from django.db import models

# Create your models here.

from datetime import datetime

class CityDict(models.Model):
    name=models.CharField(max_length=30,verbose_name='城市名称')
    desc=models.CharField(max_length=200,verbose_name='城市描述')
    add_time=models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    class Meta:
        verbose_name='城市'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.name

class CourseOrg(models.Model):
    ORG_CHOICES = (
        ("pxjg", "培训机构"),
        ("gx", "高校"),
        ("gr", "个人"),
    )
    category = models.CharField(max_length=20, choices=ORG_CHOICES, verbose_name="机构类别", default="pxjg")
    name=models.CharField(max_length=50,verbose_name='机构名称')
    desc=models.TextField(verbose_name='机构描述')
    click_nums=models.IntegerField(default=0,verbose_name='点击数')
    fav_nums=models.IntegerField(default=0,verbose_name='收藏数')
    image=models.ImageField(upload_to='org/%Y/%m',verbose_name='封面图')
    address=models.CharField(max_length=150,verbose_name='机构地址')
    city=models.ForeignKey(CityDict,verbose_name='城市')
    students = models.IntegerField("学习人数", default=0)
    course_nums = models.IntegerField("课程数", default=0)
    add_time=models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    def get_teacher_nums(self):
        # 获取机构的教师数
        return self.teacher_set.all().count()

    class Meta:
        verbose_name='课程机构'
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.name


class Teacher(models.Model):
    org=models.ForeignKey(CourseOrg,verbose_name='所属机构')
    name=models.CharField(max_length=50,verbose_name='教师名')
    work_years=models.IntegerField(default=0,verbose_name='工作年限')
    work_company=models.CharField(max_length=50,verbose_name='就职公司')
    work_position=models.CharField(max_length=50,verbose_name='公司职位')
    points=models.CharField(max_length=50,verbose_name='教学特点')
    click_nums=models.IntegerField(default=0,verbose_name='点击数')
    fav_nums=models.IntegerField(default=0,verbose_name='收藏数')
    teacher_age = models.IntegerField('年龄', default=25)
    image = models.ImageField(default='',upload_to="teacher/%Y/%m",verbose_name="头像",max_length=100)
    add_time=models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    class Meta:
        verbose_name='教师'
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.name

