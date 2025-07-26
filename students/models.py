from django.db import models
import uuid
import datetime  # 添加datetime导入
from django.contrib.auth.models import User

class Student(models.Model):
    # 删除原有的generate_student_number类方法
    # s_num = models.CharField(max_length=20, verbose_name="学生学号")  # 移除default参数
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student',null=True)
    s_num = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=20, null=True, verbose_name="学生姓名")
    username = models.CharField(max_length=20, null=True, verbose_name="学生用户名")
    password = models.CharField(max_length=128, verbose_name='密码',default='123456')
    class_num = models.CharField(max_length=64, null=True, verbose_name="学生班级号")
    phone = models.CharField(max_length=20, null=True, verbose_name="学生手机")
    email = models.CharField(max_length=64, null=True, verbose_name="学生邮箱")
    jwt = models.TextField( null=True, verbose_name="验证令牌")
    createtime = models.DateTimeField(auto_now_add=True, verbose_name="注册时间")

    class Meta:
        verbose_name = "学生"
        verbose_name_plural = "学生"

    def __str__(self):
        return f"{self.name}({self.s_num})"

    def save(self, *args, **kwargs):
        # 添加save方法生成学号
        if not self.s_num:
            today = datetime.date.today().strftime('%Y%m%d')
            count = Student.objects.filter(createtime__date=datetime.date.today()).count() + 1
            self.s_num = f"{today}{count:05d}"
        super().save(*args, **kwargs)

class Submission(models.Model):
    
    u_num = models.CharField(max_length=20, default=str(uuid.uuid4())[:8], verbose_name="提交标号")
    s_num = models.CharField(max_length=20, null=True, verbose_name="学生学号")
    h_num = models.CharField(max_length=20, null=True, verbose_name="题目序号")
    up_time = models.DateTimeField(null=True, verbose_name="提交时间")
    score = models.CharField(max_length=5, null=True, verbose_name="分数")
    advice = models.TextField(null=True, verbose_name="修改建议")
    ressuggest = models.TextField(null=True, verbose_name="资源推荐理由")
    knowledgegraph = models.CharField(max_length=64, null=True, verbose_name="知识点知识图谱")
    status = models.CharField(max_length=5, default="未提交", verbose_name="提交状态")

    class Meta:
        verbose_name = "题目文档提交"
        verbose_name_plural = "题目文档提交"

    def __str__(self):
        return f"提交 {self.u_num} (学生: {self.s_num})"
