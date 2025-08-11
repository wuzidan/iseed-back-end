import json
import os

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import JsonResponse, FileResponse
from django.shortcuts import render, redirect, get_object_or_404

from DjangoProject import settings
from goods import models
from goods.models import DocumentSubmission
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from utils.middleware import ThreadLocalStorage

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from goods.models import DocumentSubmission, WritingTopic
from django.test.client import RequestFactory
# Create your views here.


def studentlist(request):
    if request.method == 'GET':
        students = models.student.objects.all()
        return render(request,"studentlist.html",{'students':students})
    password=request.POST.get('password')
    sex=request.POST.get('sex')
    email=request.POST.get('email')
    phone=request.POST.get('phone')

    models.student.objects.create( name=request.POST.get('name'),username=request.POST.get('username'),password=password,sex=sex,email=email,phone=phone)
    students = models.student.objects.all()
    return render(request, "studentlist.html", {'students': students})

def addstudent(request):
    if request.method == 'GET':
        return render(request,"addstudent.html")
    if request.method == "POST":
        # print(request.POST)
        # student = models.student(request.POST)
        # student.save()
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.create(
            username=username,
            password=make_password(password),  # 确保密码被正确哈希
            email=request.POST.get('email', ''),
            first_name=request.POST.get('name', '')
        )
        # 创建Student并关联到User
        student = models.student(
            user=user,  # 关联到刚创建的User
            name=request.POST.get('name'),
            username=username,
            password=password,  # 可以保留，但实际登录用User的密码
            # ... other fields ...
        )
        student.save()
        # print(request.POST)
        # models.student.objects.create(name=request.POST.get('name'), username=request.POST.get('username'),
        #                               password=request.POST.get('password'), sex=request.POST.get('sex'), email=request.POST.get('email'), phone=request.POST.get('phone'))
        return redirect("/studentlist/")

def updatestudent(request):
    if request.method == 'GET':
        sid=request.GET.get('sid')
        student = models.student.objects.filter(id=sid).first()
        return render(request, "updatestudent.html", {'student':student})
    if request.method == "POST":
        sid = request.GET.get('sid')
        models.student.objects.filter(id=sid).update(name=request.POST.get('name'), username=request.POST.get('username'),
                                      password=request.POST.get('password'), sex=request.POST.get('sex'),
                                      email=request.POST.get('email'), phone=request.POST.get('phone'))
        return redirect("/studentlist/")

def deletestudent(request,sid):

    models.student.objects.filter(id=sid).delete()
    # return render(request, "studentlist.html", {'students': students})
    return redirect("/studentlist/")

def upload_document(request):
    # 仅允许POST请求
    if request.method != 'POST':
        return JsonResponse({'error': '仅支持POST请求'}, status=405)

    print(request)
    print(request.FILES)
    # 检查是否有文件上传
    if 'file' not in request.FILES:
        return JsonResponse({'error': '未找到上传文件'}, status=400)

    file = request.FILES['file']
    # 允许的文件扩展名
    allowed_extensions = ['.pdf', '.doc', '.docx', '.txt']
    # 获取文件扩展名并转换为小写
    ext = os.path.splitext(file.name)[1].lower()

    # 验证文件类型
    if ext not in allowed_extensions:
        return JsonResponse({
            'error': '不支持的文件类型',
            'allowed_types': ['pdf', 'doc', 'docx', 'txt']
        }, status=400)

    # 保存文件到媒体目录
    try:
        # 创建documents子目录（如果不存在）
        if not os.path.exists(os.path.join(settings.MEDIA_ROOT, 'documents')):
            #settings.MEDIA_ROOT 是Django项目的媒体文件目录路径（media的路径）,所有用户上传文件都放在这里
            #document是我们要创建的子目录名字，存放文档类上传文件
            #join函数把前面两个拼在一起得到完整路径
            os.makedirs(os.path.join(settings.MEDIA_ROOT, 'documents'))

        # 保存文件
        file_path = default_storage.save(f'documents/{file.name}', ContentFile(file.read()))
        #ContentFile(file.read())是把file.read()读到的二进制内容转换成django存储体系能识别的文件格式
        return JsonResponse({
            'message': '文件上传成功',
            'file_path': file_path,
            'file_url': f'{settings.MEDIA_URL}{file_path}'
        }, status=200)
    except Exception as e:
        return JsonResponse({'error': f'文件保存失败: {str(e)}'}, status=500)

# def download_document(request, upload_id):
def download_document(request):
    # 获取文件记录
    # upload = get_object_or_404(Upload, id=upload_id)
    uploaded_file = models.DocumentSubmission.objects.filter(s_num=ThreadLocalStorage.get('s_num')).first()
    file_path=uploaded_file.path
    # 构建完整文件路径
    # file_path = os.path.join(settings.MEDIA_ROOT, upload.path)
    # file_path = "C:\\Users\lijunze\PycharmProjects\DjangoProject\media\documents\毕业生档案派遣申请表.docx"
    # 验证文件是否存在
    if not os.path.exists(file_path):
        return JsonResponse({'error': '文件不存在'}, status=404)
    
    # 验证文件是否可读取
    if not os.path.isfile(file_path) or not os.access(file_path, os.R_OK):
        return JsonResponse({'error': '无法读取文件'}, status=403)

    # 从文件路径提取扩展名
    file_ext = os.path.splitext(file_path)[1].lower()

    # 根据扩展名映射MIME类型
    mime_types = {
        '.pdf': 'application/pdf',
        '.doc': 'application/msword',
        '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        '.txt': 'text/plain'
    }
    # 获取内容类型，默认为二进制流
    content_type = mime_types.get(file_ext, 'application/octet-stream')
    # 设置响应内容类型
    # content_type = ''
    # if upload.file_type == 'PDF':
    #     content_type = 'application/pdf'
    # elif upload.file_type in ['DOC', 'DOCX']:
    #     content_type = 'application/msword'
    # elif upload.file_type == 'TXT':
    #     content_type = 'text/plain'
    
    # 返回文件响应
    response = FileResponse(open(file_path, 'rb'), content_type=content_type)
    response['Content-Disposition'] = f'attachment; filename="{file_path}"'
    return response


# def add_document(request):
#     if request.method == 'POST':
#         submission = DocumentSubmission()
#         # 直接存储学号字符串，无需查询学生表
#         submission.s_num = request.POST.get('s_num')
#         submission.t_num = request.POST.get('t_num')
#         submission.up_time = timezone.now()
#         submission.status = request.POST.get('status')
#         submission.advice = request.POST.get('advice')
#         submission.ressuggest = request.POST.get('ressuggest')
#
#         # 处理知识图谱文件上传
#         if 'knowledgegraph' in request.FILES:
#             file = request.FILES['knowledgegraph']
#             file_path = f'documents/{file.name}'
#             with open(f'media/{file_path}', 'wb+') as destination:
#                 for chunk in file.chunks():
#                     destination.write(chunk)
#             submission.knowledgegraph = file_path
#
#         submission.save()
#         return redirect('document_list')
#     else:
#         # 获取所有题目列表
#         topics = WritingTopic.objects.all()
#         return render(request, 'adddocument.html', {'topics': topics})
#
#     # 移除学生列表查询，无需下拉选择
#     return render(request, 'adddocument.html')

def add_document(request):
    # if request.method == 'GET':
    #     return render(request, "adddocument.html",{'snum':ThreadLocalStorage.get('s_num')})
    if request.method == 'POST':
        submission = DocumentSubmission()
        submission.s_num = request.POST.get('s_num')
        submission.up_time = timezone.now()
        submission.status = request.POST.get('status')
        submission.advice = request.POST.get('advice', '')
        submission.ressuggest = request.POST.get('ressuggest', '')

        # 处理题目选择逻辑
        topic_id = request.POST.get('topic_id')
        if topic_id == 'other':
            # 获取用户输入的新题目信息
            other_title = request.POST.get('other_title')
            other_des = request.POST.get('other_des')

            # 验证新题目信息
            if not other_title or not other_des:
                messages.error(request, '新题目标题和描述不能为空')
                return redirect('/adddocument/')

            # 创建新题目并保存到数据库
            try:
                new_topic = WritingTopic.objects.create(
                    # t_num=f'other_{submission.s_num}',  # 使用学生学号生成临时教师编号
                    title=other_title,
                    des=other_des,
                    # types='其他',  # 设置默认类型
                    # s_up=True  # 标记为学生上传的题目
                )
                # 使用新题目的t_num
                # submission.t_num = new_topic.t_num
            except Exception as e:
                messages.error(request, f'创建新题目失败: {str(e)}')
                return redirect('/adddocument/')
        else:
            # 选择已有题目
            try:
                topic = WritingTopic.objects.get(id=topic_id)
                # submission.t_num = topic.t_num
            except WritingTopic.DoesNotExist:
                messages.error(request, '所选题目不存在')
                return redirect('/adddocument/')

        # # 处理知识图谱文件上传
        # if 'knowledgegraph' in request.FILES:
        #     file = request.FILES['knowledgegraph']
        #     file_path = f'documents/{file.name}'
        #     with open(f'media/{file_path}', 'wb+') as destination:
        #         for chunk in file.chunks():
        #             destination.write(chunk)
        #     submission.knowledgegraph = file_path
        #     # 处理文件上传
        # if 'file' in request.FILES:
        #     file = request.FILES['file']
        #     # 创建上传目录（如果不存在）
        #     upload_dir = os.path.join(settings.MEDIA_ROOT, 'documents')
        #     os.makedirs(upload_dir, exist_ok=True)
        #
        #     # 保存文件并获取绝对路径
        #     file_path = os.path.join(upload_dir, file.name)
        #     with open(file_path, 'wb+') as destination:
        #         for chunk in file.chunks():
        #             destination.write(chunk)
        #
        #     # 设置文件名和绝对路径
        #     submission.filename = file.name
        #     submission.path = file_path
        # 调用upload_document处理文件上传
        print(request.FILES)
        if 'file' in request.FILES:
            # 创建请求工厂
            factory = RequestFactory()
            # 构造包含文件的POST请求
            post_request = factory.post('/upload_document/', {'file': request.FILES['file']})
            # 调用upload_document函数
            response = upload_document(post_request)

            # 解析响应结果
            if response.status_code == 200:
                data = json.loads(response.content)
                # 获取文件名和路径
                submission.filename = os.path.basename(data['file_path'])
                submission.path = os.path.join(settings.MEDIA_ROOT, data['file_path'])  # 绝对路径
            else:
                # 处理上传错误
                error_msg = response.json().get('error', '文件上传失败')
                messages.error(request, error_msg)
                return render(request, 'adddocument.html', {'error': error_msg})
        submission.save()
        return redirect('/adddocument/')
    else:
        # 打开页面时查询所有题目
        topics = WritingTopic.objects.all()
        return render(request, 'adddocument.html', {'topics': topics})

def login_student(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        print(username, password)
        # 使用Django内置认证系统验证用户
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # 登录用户
            login(request, user)
            try:
                # 通过关联关系获取学生信息
                student = user.student
                # 存储学生信息到线程
                ThreadLocalStorage.set('student_id', student.id)
                ThreadLocalStorage.set('snum', student.snum)
                ThreadLocalStorage.set('username', student.username)
                messages.success(request, '登录成功！')
                return redirect('/studentlist/')
            except models.student.DoesNotExist:
                messages.error(request, '该用户没有关联的学生信息')
        else:
            messages.error(request, '用户名或密码不正确')

    return render(request, 'login.html')
        # try:
        #     # 查找学生
        #     student = models.student.objects.get(username=username)
        #     # 验证密码
        #     if check_password(password, student.password):
        #         # 登录成功，存储学生信息到线程
        #         ThreadLocalStorage.set('student_id', student.id)
        #         ThreadLocalStorage.set('snum', student.snum)
        #         ThreadLocalStorage.set('username', student.username)
        #         messages.success(request, '登录成功！')
        #         return redirect('student_dashboard')  # 重定向到学生仪表板
        #     else:
        #         messages.error(request, '用户名或密码不正确')
        # except models.student.DoesNotExist:
        #     messages.error(request, '用户名或密码不正确')

    # return render(request, 'login.html')

# 添加学生仪表板视图用于测试
def student_dashboard(request):
    # from .middleware import ThreadLocalStorage
    from utils.middleware import ThreadLocalStorage
    student_id = ThreadLocalStorage.get('student_id')
    s_num = ThreadLocalStorage.get('s_num')
    username = ThreadLocalStorage.get('username')

    if not student_id:
        messages.error(request, '请先登录')
        return redirect('login')

    return render(request, 'dashboard.html', {
        'student_id': student_id,
        's_num': s_num,
        'username': username
    })

from utils.middleware import ThreadLocalStorage
def student_submissions(request):

    s_num = ThreadLocalStorage.get('s_num')

    if not s_num:
        messages.error(request, '请先登录')
        return redirect('login')

    # 根据学号查询提交记录
    submissions = DocumentSubmission.objects.filter(s_num=s_num).order_by('-up_time')

    return render(request, 'submission_list.html', {
        'submissions': submissions,
        'student_id': ThreadLocalStorage.get('student_id'),
        'username': ThreadLocalStorage.get('username')
    })