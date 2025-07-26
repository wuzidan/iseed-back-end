from django.db import models, transaction
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.
class books(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class student(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student', null=True)
    name = models.CharField(max_length=20)
    age = models.IntegerField(null=True)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    snum = models.CharField(max_length=20)
    def save(self, *args, **kwargs):
            if not self.snum:
                # 获取当前日期字符串(YYYYMMDD)
                today = timezone.now().strftime('%Y%m%d')
                # 查询今天创建的学生数量
                today_count = student.objects.filter(
                    rdate__year=timezone.now().year,
                    rdate__month=timezone.now().month,
                    rdate__day=timezone.now().day
                ).count() + 1
                # 生成5位序号(不足补零)
                serial_number = f'{today_count:05d}'
                # 组合生成s_num
                self.snum = f'{today}{serial_number}'
            super().save(*args, **kwargs)

    sex = models.CharField(max_length=5,null=True)


    email = models.EmailField()
    phone = models.CharField(max_length=20)
    rdate = models.DateField(auto_now_add=True)
    lastlogin = models.DateTimeField(null=True)
    is_available = models.BooleanField(null=True)
    is_active = models.BooleanField(null=True)
    level_choices = (
    (1,'初学'),(2,'进阶')
    )

    level = models.IntegerField(null=True,choices=level_choices,default=1)
    jwt = models.CharField(max_length=255, null=True)

class DocumentSubmission(models.Model):
    status_choices = (
        ('未提交', '未提交'),
        ('草稿', '草稿'),
        ('已提交', '已提交')
    )
    id = models.AutoField(primary_key=True)
    u_num = models.CharField(max_length=20, null=True, verbose_name='提交标号')
    #  添加自动生成u_num的save方法

    def save(self, *args, **kwargs):
        if not self.u_num:
            # 获取当前日期字符串(YYYYMMDD)
            today = timezone.now().strftime('%Y%m%d')
            # 使用事务确保计数准确性
            with transaction.atomic():
                # 查询今天创建的提交记录数量
                today_count = DocumentSubmission.objects.select_for_update().filter(
                    up_time__year=timezone.now().year,
                    up_time__month=timezone.now().month,
                    up_time__day=timezone.now().day
                ).count() + 1
            # 生成5位序号(不足补零)
            serial_number = f'{today_count:05d}'
            # 组合生成u_num，前缀'S'表示提交记录
            self.u_num = f'S{today}{serial_number}'
        super().save(*args, **kwargs)
    # 修改为普通字符字段存储学号，不设置外键
    s_num = models.CharField(max_length=20, null=True, verbose_name='学生学号')
    t_num = models.CharField(max_length=20, null=True, verbose_name='题目标号')
    up_time = models.DateTimeField(null=True, verbose_name='提交时间')
    score = models.CharField(max_length=5, null=True, verbose_name='分数')
    advice = models.TextField(null=True, verbose_name='修改建议')
    ressuggest = models.TextField(null=True, verbose_name='资源推荐理由')
    knowledgegraph = models.CharField(max_length=64, null=True, verbose_name='知识图谱路径')
    status = models.CharField(max_length=5, choices=status_choices, default='未提交', verbose_name='提交状态')
    filename = models.CharField(max_length=255, null=True, verbose_name='文件名')
    path = models.CharField(max_length=512, null=True, verbose_name='文件路径')

class WritingTopic(models.Model):
    id = models.AutoField(primary_key=True)
    # t_num = models.CharField(max_length=50, verbose_name="教师编号")
    title = models.CharField(max_length=255, verbose_name="题目标题")
    des = models.TextField(verbose_name="题目描述")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    types = models.CharField(max_length=50, verbose_name="题目类型")
    # s_up = models.BooleanField(default=False, verbose_name="学生上传")
    # doc_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="文档名称")
    # d_path = models.CharField(max_length=512, blank=True, null=True, verbose_name="文档路径")

    class Meta:
        verbose_name = "写作题目"
        verbose_name_plural = "写作题目"

    def __str__(self):
        return self.title