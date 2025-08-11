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
    # 状态选项元组定义
    STATUS_CHOICES = [
        (0, "未通过该关卡"),
        (1, "用户提交结果正在评测"),
        (2, "用户通过该关卡"),
        (3, "用户未开启本关卡")
    ]
    ANSWER_OPEN_CHOICES = [
        (0, "未查看参考答案"),
        (1, "已查看参考答案")
    ]
    # CONDITION_CHOICES = [
    #     (0, "未提交"),
    #     (1, "已提交"),
    #     (2, "已批改")
    # ]

    u_num = models.CharField(max_length=20, verbose_name="提交标号")
    s_num = models.CharField(max_length=20, null=True, verbose_name="学生学号")
    h_num = models.CharField(max_length=20, null=True, verbose_name="题目序号")
    up_time = models.DateTimeField(null=True, verbose_name="提交时间")
    up_fname = models.CharField(max_length=255, null=True, default='', verbose_name="文件名")
    up_path = models.TextField(null=True, verbose_name="提交文件路径")
    createtime = models.DateTimeField(auto_now_add=True,null=True, verbose_name="创建时间")
    updatetime = models.DateTimeField(auto_now=True, verbose_name="修改时间")
    open_time = models.DateTimeField(null=True, verbose_name="交互开启时间")
    end_time = models.DateTimeField(null=True, verbose_name="交互结束时间")
    star = models.CharField(max_length=5, null=True, verbose_name="关卡评分")
    answer_open = models.IntegerField(choices=ANSWER_OPEN_CHOICES, default=0, verbose_name="是否查看参考答案")
    evaluate_count = models.CharField(max_length=5, default='0', verbose_name="用户评测次数")
    score = models.CharField(max_length=5, null=True, verbose_name="分数")
    advice = models.TextField(null=True, verbose_name="修改建议")
    ressuggest = models.TextField(null=True, verbose_name="资源推荐理由")
    knowledgegraph = models.CharField(max_length=64, null=True, verbose_name="知识点知识图谱")
    status = models.IntegerField(choices=STATUS_CHOICES, default=0, verbose_name="评测状态")
    condition = models.CharField(max_length=5, default="未提交", verbose_name="提交状态")

    class Meta:
        verbose_name = "题目文档提交"
        verbose_name_plural = "题目文档提交"

    def __str__(self): 
        return f"提交 {self.u_num} (学生: {self.s_num})"

    def save(self, *args, **kwargs):
        # 系统生成班级号：年月日+当日序号（如2023102701）
        if not self.u_num:
            today = datetime.date.today().strftime('%Y%m%d')
            count = Submission.objects.filter(createtime__date=datetime.date.today()).count() + 1
            self.u_num = f"Sub{today}{count:05d}"
        super().save(*args, **kwargs)
