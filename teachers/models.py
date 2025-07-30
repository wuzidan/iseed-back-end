import datetime
from django.db import models
import uuid
from django.contrib.auth.models import User

class Teacher(models.Model):
    # 删除原有的generate_teacher_number类方法
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher', null=True)
    t_num = models.CharField(max_length=20, verbose_name="老师工号")  # 移除default参数
    name = models.CharField(max_length=20, null=True, verbose_name="老师姓名")
    username = models.CharField(max_length=20, null=True, verbose_name="老师用户名")
    password = models.CharField(max_length=128, verbose_name='密码',default='123456')
    phone = models.CharField(max_length=20, null=True, verbose_name="老师手机")
    email = models.CharField(max_length=64, null=True, verbose_name="老师邮箱")
    jwt = models.TextField( null=True, verbose_name="验证令牌")
    createtime = models.DateTimeField(auto_now_add=True, verbose_name="注册时间")

    class Meta:
        verbose_name = "教师"
        verbose_name_plural = "教师"

    def __str__(self):
        return f"{self.name}({self.t_num})"

    def save(self, *args, **kwargs):
        # 添加save方法生成工号
        if not self.t_num:
            today = datetime.date.today().strftime('%Y%m%d')
            count = Teacher.objects.filter(createtime__date=datetime.date.today()).count() + 1
            self.t_num = f"{today}{count:05d}"
        super().save(*args, **kwargs)

class Course(models.Model):
    
    l_num = models.CharField(max_length=20, verbose_name="课程号")
    title = models.CharField(max_length=20, null=True, verbose_name="课程名")
    t_num = models.CharField(max_length=20, null=True, verbose_name="教师工号")
    des = models.TextField(null=True, verbose_name="课程描述")
    type = models.CharField(max_length=64, null=True, verbose_name="课程类型")
    credit = models.IntegerField(null=True, verbose_name="课程学分")
    createtime = models.DateTimeField(auto_now_add=True, verbose_name="注册时间")
    updatetime = models.DateTimeField(auto_now=True, verbose_name="修改时间")

    class Meta:
        verbose_name = "课程"
        verbose_name_plural = "课程"

    def save(self, *args, **kwargs):
        # 系统生成班级号：年月日+当日序号（如2023102701）
        if not self.l_num:
            today = datetime.date.today().strftime('%Y%m%d')
            count = Course.objects.filter(createtime__date=datetime.date.today()).count() + 1
            self.l_num = f"{today}{count:05d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Class(models.Model):
    
    c_num = models.CharField(max_length=20, verbose_name="班级号")  # 移除默认UUID
    c_name = models.CharField(max_length=20, null=True, verbose_name="班级名")
    t_num = models.CharField(max_length=20, null=True, verbose_name="教师工号")
    grade = models.CharField(max_length=20, null=True, verbose_name="所属年级")
    number = models.IntegerField(null=True, verbose_name="班级人数")
    createtime = models.DateTimeField(auto_now_add=True, verbose_name="注册时间")
    updatetime = models.DateTimeField(auto_now=True, verbose_name="修改时间")

    class Meta:
        verbose_name = "班级"
        verbose_name_plural = "班级"
        ordering = ['c_name']

    def save(self, *args, **kwargs):
        # 系统生成班级号：年月日+当日序号（如2023102701）
        if not self.c_num:
            today = datetime.date.today().strftime('%Y%m%d')
            count = Class.objects.filter(createtime__date=datetime.date.today()).count() + 1
            self.c_num = f"{today}{count:05d}"
        super().save(*args, **kwargs)
    def __str__(self):
        return self.c_name

class CourseResource(models.Model):
    
    r_num = models.CharField(max_length=20, verbose_name="资源序号")
    l_num = models.CharField(max_length=20, null=True, verbose_name="课程号")
    r_title = models.TextField(null=True, verbose_name="课程资源标题")
    r_des = models.TextField(null=True, verbose_name="课课程资源简介")
    r_path = models.CharField(max_length=255, null=True, verbose_name="文件存储路径")
    r_type = models.CharField(max_length=20, null=True, verbose_name="文件类型")
    createtime = models.DateTimeField(auto_now_add=True, verbose_name="注册时间")

    def save(self, *args, **kwargs):
        # 系统生成作业号
        if not self.r_num:
            today = datetime.date.today().strftime('%Y%m%d')
            count = CourseResource.objects.filter(createtime__date=datetime.date.today()).count() + 1
            self.r_num = f"CR{today}{count:05d}"
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "课程资源"
        verbose_name_plural = "课程资源"

    def __str__(self):
        return self.r_name

class Homework(models.Model):
    
    h_num = models.CharField(max_length=20, verbose_name="作业号")
    l_num = models.CharField(max_length=20, null=True, verbose_name="课程号")
    title = models.CharField(max_length=20, null=True, verbose_name="作业标题")
    des = models.TextField(null=True, verbose_name="作业详细说明")
    hd_name = models.CharField(max_length=64, null=True, verbose_name="作业文件名")
    hd_path = models.CharField(max_length=255, null=True, verbose_name="作业文件存储路径")
    hd_type = models.CharField(max_length=20, null=True, verbose_name="文件类型")
    createtime = models.DateTimeField(auto_now_add=True, verbose_name="注册时间")
    updatetime = models.DateTimeField(auto_now=True, verbose_name="修改时间")

    class Meta:
        verbose_name = "作业"
        verbose_name_plural = "作业"

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # 系统生成作业号
        if not self.h_num:
            today = datetime.date.today().strftime('%Y%m%d')
            count = Homework.objects.filter(createtime__date=datetime.date.today()).count() + 1
            self.h_num = f"H{today}{count:05d}"
        super().save(*args, **kwargs)

class CourseEnrollment(models.Model):
    
    o_num = models.CharField(max_length=20,  verbose_name="选修号")
    c_num = models.CharField(max_length=20, null=True, verbose_name="班级号")
    l_num = models.CharField(max_length=20, null=True, verbose_name="课程号")
    createtime = models.DateTimeField(auto_now_add=True, verbose_name="注册时间")

    class Meta:
        verbose_name = "班级课程选修"
        verbose_name_plural = "班级课程选修"
        unique_together = ("c_num", "l_num")  # 确保班级和课程的组合唯一

    def save(self, *args, **kwargs):
        # 系统生成班级号：年月日+当日序号（如2023102701）
        if not self.o_num:
            today = datetime.date.today().strftime('%Y%m%d')
            count = CourseEnrollment.objects.filter(createtime__date=datetime.date.today()).count() + 1
            self.o_num = f"CE{today}{count:05d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"选修 {self.o_num} (班级: {self.c_num}, 课程: {self.l_num})"
