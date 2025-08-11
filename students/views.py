import jwt
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.exceptions import TokenError

from DjangoProject import settings
from .models import Student
from utils.middleware import ThreadLocalStorage
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth import login
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
from utils import custom_jwt
import os
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from utils.up_down_doc import upload_document
from teachers.models import Course, Homework, CourseResource, CourseEnrollment
from rest_framework import status
from .serializers import CourseSerializer
from .models import Submission
from goods.models import DocumentSubmission
from utils.up_down_doc import download_document
from .serializers import SubmissionSerializer, HomeworkSerializer
import base64
import mimetypes

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Student
from .serializers import StudentSerializer
from goods.models import DocumentSubmission
from .serializers import DocumentSubmissionSerializer

from .models import Submission
from .serializers import SubmissionSerializer

# 学生登录验证
@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny])
def student_login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            student = student1 = Student.objects.get(username=username)

            # print(str1.access_token)
            # try:
            #     str1.verify()
            #     print('过')
            #     pass
            # except TokenError as e:
            #     return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
            # payload = jwt.decode(str(str1.access_token),settings.SECRET_KEY,algorithms=['HS256'])
            # print(payload)

            if check_password(password, student.password):
                print(student)
                # 检查并创建User关联
                if not student.user:
                    user = User.objects.create_user(
                        username=student.username,
                        password=password
                    )
                    student.user = user
                    student.save()
                student.jwt = str(custom_jwt.CustomTokenObtainPairSerializer.get_token(student1))
                print(student.jwt)
                student.save()
                # 设置线程本地存储
                ThreadLocalStorage.set('user_type', 'student')
                ThreadLocalStorage.set('user_id', student.id)
                ThreadLocalStorage.set('user_num', student.s_num)
                ThreadLocalStorage.set('username', student.username)

                return Response({
                    'success': True,
                    'message': '登录成功',
                    'data': {
                        'jwt': student.jwt,
                        'username': student.username,
                        'name': student.name,
                        'class_num': student.class_num
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'success': False,
                    'message': '密码错误'
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Student.DoesNotExist:
            return Response({
                'success': False,
                'message': '用户名不存在'
            }, status=status.HTTP_404_NOT_FOUND)

    return Response({
        'success': False,
        'message': '请使用POST方法'
    }, status=status.HTTP_405_METHOD_NOT_ALLOWED)

# 学生信息编辑
@api_view(['POST'])
@csrf_exempt
# @permission_classes([AllowAny])
def student_edit(request):
    if request.method == 'POST':
        # 从线程存储获取当前用户学号
        id = ThreadLocalStorage.get('user_id')

        student = Student.objects.get(id=id)
        s_num = student.s_num
        username = student.username
        if student is None:
            return Response({
                'success': False,
                'message': '用户未登录或会话已过期'
            }, status=status.HTTP_401_UNAUTHORIZED)

        try:
            # student = Student.objects.get(s_num=s_num)
            # 定义可更新的字段列表
            updatable_fields = ['name', 'username', 'class_num', 'phone', 'email']

            # 遍历字段进行条件更新
            for field in updatable_fields:
                # 获取前端传递的字段值
                value = request.data.get(field)
                # 仅当字段存在且值不为空时更新
                if value is not None and value != '':
                    setattr(student, field, value)
            student.save()

            return Response({
                'success': True,
                'message': '信息更新成功',
                'data': {
                    's_num': student.s_num,
                    'name': student.name,
                    'username': student.username,
                    'class_num': student.class_num,
                    'phone': student.phone,
                    'email': student.email
                }
            }, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            return Response({
                'success': False,
                'message': '学生不存在'
            }, status=status.HTTP_404_NOT_FOUND)

    return Response({
        'success': False,
        'message': '请使用POST方法'
    }, status=status.HTTP_405_METHOD_NOT_ALLOWED)

# 学生密码修改
@api_view(['POST'])
@csrf_exempt
# @permission_classes([AllowAny])
def student_change_password(request):
    if request.method == 'POST':
        # 从线程存储获取当前用户学号
        id = ThreadLocalStorage.get('user_id')

        student = Student.objects.get(id=id)
        s_num = student.s_num
        username = student.username

        if student is None:
            return Response({
                'success': False,
                'message': '用户未登录或会话已过期'
            }, status=status.HTTP_401_UNAUTHORIZED)

        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        try:
            student = Student.objects.get(s_num=s_num)
            if check_password(old_password, student.password):
                student.password = make_password(new_password)
                student.save()
                return Response({
                    'success': True,
                    'message': '密码修改成功'
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'success': False,
                    'message': '原密码错误'
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Student.DoesNotExist:
            return Response({
                'success': False,
                'message': '学号不存在'
            }, status=status.HTTP_404_NOT_FOUND)

    return Response({
        'success': False,
        'message': '请使用POST方法'
    }, status=status.HTTP_405_METHOD_NOT_ALLOWED)

# 获取学生课程信息
@api_view(['GET'])
def get_courses(request):
    # 获取当前学生信息
    student_id = ThreadLocalStorage.get('user_id')
    if not student_id:
        return Response({
            'success': False,
            'message': '用户未登录'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        student = Student.objects.get(id=student_id)
        class_num = student.class_num
        
        # 获取班级选修的课程
        enrollments = CourseEnrollment.objects.filter(c_num=class_num)
        course_nums = [enrollment.l_num for enrollment in enrollments]
        print(f"课程编号列表: {course_nums}")
        
        # 获取课程信息及相关资源
        courses = Course.objects.filter(l_num__in=course_nums)
        serializer = CourseSerializer(courses, many=True)
        
        return Response({
            'success': True,
            'data': serializer.data
        })
    except Student.DoesNotExist:
        return Response({
            'success': False,
            'message': '学生不存在'
        }, status=status.HTTP_404_NOT_FOUND)

# 学生注册功能
@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny])
def student_register(request):
    if request.method == 'POST':
        # 获取必填字段
        username = request.data.get('username')
        password = request.data.get('password')
        name = request.data.get('name')

        # 验证必填字段
        if not all([username, password, name]):
            return Response({
                'success': False,
                'message': '用户名、密码和姓名为必填项'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 验证用户名唯一性
        if Student.objects.filter(username=username).exists() or User.objects.filter(username=username).exists():
            return Response({
                'success': False,
                'message': '用户名已存在'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 创建Django User对象
        user = User.objects.create_user(
            username=username,
            password=password,
            email=request.data.get('email', '')
        )

        # 创建学生对象并关联User
        student = Student(
            user=user,  # 关联User
            username=username,
            password=make_password(password),  # 保持原密码字段
            name=name,
            # 处理非必填字段
            class_num=request.data.get('class_num'),
            phone=request.data.get('phone'),
            email=request.data.get('email')
        )
        student.save()

        return Response({
            'success': True,
            'message': '学生注册成功',
            'data': {
                'student_id': student.id,
                'username': student.username,
                'name': student.name,
                's_num': student.s_num
            }
        }, status=status.HTTP_201_CREATED)

    return Response({
        'success': False,
        'message': '请使用POST方法'
    }, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
@permission_classes([AllowAny])
@transaction.atomic
def upload_homework(request):
    # 获取请求参数
    file = request.FILES.get('file')
    h_num = request.POST.get('h_num')
    l_num = request.POST.get('l_num')
    title = request.POST.get('title')
    des = request.POST.get('des')
    # 获取请求数据
    # 获取前端传递的新字段
    answer_open = request.POST.get('answer_open')
    open_time = request.POST.get('open_time')
    end_time = request.POST.get('end_time')
    star = request.POST.get('star', 0)
    id = ThreadLocalStorage.get('user_id')
    student = Student.objects.get(id=id)
    s_num = student.s_num
    # 计算evaluate_count: 根据s_num和h_num查询提交记录数量+1
    existing_count = Submission.objects.filter(s_num=s_num, h_num=h_num).count()
    evaluate_count = existing_count + 1
     # 从登录用户获取学生学号
    id = ThreadLocalStorage.get('user_id')
    student = Student.objects.get(id=id)
    s_num = student.s_num
    # 基础验证
    if not file:
        return Response({
            'success': False,
            'message': '请上传作业文件'
        }, status=400)

    # 验证课程号是否存在
    # if not l_num or not Course.objects.filter(l_num=l_num).exists():
    #     return Response({
    #         'success': False,
    #         'message': '课程号不存在或未提供'
    #     }, status=400)

    # 处理作业信息（存在则获取，不存在则创建）
    homework = None
    if h_num:
        homework = Homework.objects.filter(h_num=h_num).first()
    # 创建提交记录前检查重复提交
    if homework:
        existing_submission = Submission.objects.filter(
            s_num=s_num,
            h_num=homework.h_num
        ).first()
        if existing_submission:
            return Response({
                'success': False,
                'message': f'该作业已提交（提交编号：{existing_submission.u_num}），请勿重复提交',
                'existing_submission_id': existing_submission.u_num
            }, status=400)
    # 创建新作业（如果需要）
    if not homework:
        if not title:
            return Response({
                'success': False,
                'message': '新作业必须提供标题'
            }, status=400)

        homework = Homework.objects.create(
            l_num=l_num or '',
            title=title,
            des=des or '',

        )

    # 上传文件（使用通用上传函数）
    allowed_types = ['.pdf', '.doc', '.docx', '.txt']
    save_dir = os.path.join('media', 'homework_submissions', homework.h_num)
    # filename = f"{s_num}_{timezone.now().strftime('%Y%m%d%H%M%S')}{os.path.splitext(file.name)[1]}"
    filename = f"{s_num}_{timezone.now().strftime('%Y%m%d%H%M%S')}{file.name}"
    # filename = f"{file.name}"

    upload_result = upload_document(
        file=file,
        save_dir=save_dir,
        filename=filename,
        allowed_types=allowed_types
    )

    if not upload_result['success']:
        return Response(upload_result, status=400)

    # 创建提交记录
    submission = Submission.objects.create(
        s_num=s_num,
        h_num=homework.h_num,
        up_time=timezone.now(),
        status=1,  #
        condition='已提交',
        up_fname=filename,
        up_path=upload_result['path'],
        # 初始化新增字段的默认值
        answer_open=answer_open,
        evaluate_count=evaluate_count,
        open_time=open_time,
        end_time=end_time,
        star=int(star) if star else 0,
    )

    return Response({
        'success': True,
        'message': '作业提交成功',
        'data': {
            'submission_id': submission.u_num,
            'homework_id': homework.h_num,
            'file_path': upload_result['path']
        }
    })


# 获取提交记录
@api_view(['GET'])
@permission_classes([AllowAny])
def get_submission_records(request):
    """
    获取学生作业提交记录及文件（JSON包含Base64编码的文件内容）
    """
    # 从ThreadLocal获取当前学生信息
    student_id = ThreadLocalStorage.get('user_id')
    if not student_id:
        return Response({
            'success': False,
            'message': '用户未登录或会话已过期'
        }, status=status.HTTP_401_UNAUTHORIZED)

    try:
        student = Student.objects.get(id=student_id)
        s_num = student.s_num
    except Student.DoesNotExist:
        return Response({
            'success': False,
            'message': '学生信息不存在'
        }, status=status.HTTP_404_NOT_FOUND)

    # 获取请求参数
    u_num = request.query_params.get('u_num')
    h_num = request.query_params.get('h_num')

    # 参数验证
    if not u_num and not h_num:
        return Response({
            'success': False,
            'message': '必须提供u_num或h_num参数'
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        # 查询提交记录
        if u_num:
            submission = Submission.objects.get(u_num=u_num, s_num=s_num)
        else:
            submission = Submission.objects.filter(s_num=s_num, h_num=h_num).order_by('-up_time').first()
            
        if not submission:
            return Response({
                'status': 'error', 
                'message': '未找到提交记录'
            }, status=404)
        
        # 使用序列化器转换为JSON可序列化数据
        serializer = SubmissionSerializer(submission)
        return Response({
            'status': 'success',
            'data': serializer.data
        })
    
    except Submission.DoesNotExist:
        return Response({
            'status': 'error', 
            'message': '未找到提交记录'
        }, status=404)
    except Exception as e:
        return Response({
            'status': 'error', 
            'message': str(e)
        }, status=500)
    except Submission.MultipleObjectsReturned:
        return Response({
            'success': False,
            'message': '找到多条提交记录，请使用u_num精确查询'
        }, status=status.HTTP_400_BAD_REQUEST)

    # 准备基础响应数据
    # response_data = {
    #     'success': True,
    #     'message': '提交记录获取成功',
    #     'data':submission
        # 'data': {
        #     'u_num': submission.u_num,
        #     's_num': submission.s_num,
        #     'h_num': submission.h_num,
        #     'up_path': submission.up_path,
        #     'up_time': submission.up_time.isoformat() if submission.up_time else None,
        #     'up_fname': submission.up_fname,
        #     'status': submission.get_status_display(),  # 返回状态文本描述
        #     'condition': submission.condition,  # 新增字段：提交状态文本
        #     'score': submission.score,
        #     'advice': submission.advice,
        #     'star': submission.star,
        #     'open_time': submission.open_time,
        #     'end_time': submission.end_time,
        #     'answer_open': submission.answer_open,
        #     'evaluate_count': submission.evaluate_count,
        #     'createtime': submission.createtime.isoformat() if submission.createtime else None,
        # }
    # }

    # # 如果有文件路径，则添加Base64编码的文件内容
    # if submission.up_path and os.path.exists(submission.up_path):
    #     fileresponse = download_document(submission.up_path)
    #     if  fileresponse['success']:
    #         response_data['data']['fileresponse'] = fileresponse['file_response']
    #     else:
    #         response_data['data']['fileresponse'] = None
    #         response_data['message'] = '提交记录获取成功' + fileresponse['message']
        # try:
        #     # 获取MIME类型
        #     mime_type, _ = mimetypes.guess_type(submission.up_path)
        #
        #     # 读取文件并编码为Base64
        #     with open(submission.up_path, 'rb') as f:
        #         file_content = base64.b64encode(f.read()).decode('utf-8')
        #
        #
        #     # 添加文件信息到响应
        #     response_data['data']['file_info'] = {
        #         'file_name': submission.up_fname,
        #         'mime_type': mime_type or 'application/octet-stream',
        #         'base64_content': file_content
        #     }
        # except Exception as e:
        #     response_data['message'] = f'提交记录获取成功，但文件读取失败: {str(e)}'

    # return Response(response_data)

# 获取提交文件
@api_view(['POST'])
@permission_classes([AllowAny])
def get_submission_document(request):
    up_path=request.data.get('path')
    print(up_path)
    # 如果有文件路径，则添加Base64编码的文件内容
    if up_path and os.path.exists(up_path):
        fileresponse = download_document(up_path)
        print(fileresponse)
        if fileresponse['success']:
            response = fileresponse['file_response']
            return response
        else:
            return Response({
                'success': False,
                'message': fileresponse['message']
            }, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({
            'success': False,
            'message': f'文件路径错误：{up_path}'
        }, status=status.HTTP_400_BAD_REQUEST)

# 获取学生信息
@api_view(['GET'])
@permission_classes([AllowAny])
def get_student_info(request,s_num=None):
    try:
        # 从请求中获取学生ID或学号
        if s_num:
            student = Student.objects.get(s_num=s_num)
        else:
            # 如果没有提供学号，获取当前登录学生
            user_id = ThreadLocalStorage.get('user_id')
            student = Student.objects.get(id=user_id)

        serializer = StudentSerializer(student)
        return Response(serializer.data)
    except Student.DoesNotExist:
        return Response({'error': '学生不存在'}, status=status.HTTP_404_NOT_FOUND)

# 修改学生信息
@api_view(['POST'])
@permission_classes([AllowAny])
def update_student_info(request, s_num):
    try:
        student = Student.objects.get(s_num=s_num)
        serializer = StudentSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Student.DoesNotExist:
        return Response({'error': '学生不存在'}, status=status.HTTP_404_NOT_FOUND)

# 获取课程信息
@api_view(['GET'])
@permission_classes([AllowAny])
def get_student_courses(request, s_num):
    try:
        # 获取学生信息以确定所在班级
        student = Student.objects.get(s_num=s_num)
        # 查询班级选修的所有课程
        enrollments = CourseEnrollment.objects.filter(c_num=student.class_num)
        course_nums = [enrollment.l_num for enrollment in enrollments]
        # 获取课程详情及关联的作业和资源
        courses = Course.objects.filter(l_num__in=course_nums)
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)
    except Student.DoesNotExist:
        return Response({'error': '学生不存在'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 获取作业信息
@api_view(['GET'])
@permission_classes([AllowAny])
def get_student_homeworks(request, s_num):
    try:
        # 通过学号获取学生信息
        student = Student.objects.get(s_num=s_num)
        # 获取学生所在班级
        class_num = student.class_num
        print(f"学生班级: {class_num}")
        
        # 通过班级号查询所有关联的课程
        enrollments = CourseEnrollment.objects.filter(c_num=class_num)
        course_nums = [enrollment.l_num for enrollment in enrollments]
        
        # 获取课程对象列表
        courses = Course.objects.filter(l_num__in=course_nums)
        # 通过课程外键关联查询作业
        # 同时支持外键关联和课程号匹配查询
        homeworks = Homework.objects.filter(
            Q(course__in=courses) | Q(l_num__in=course_nums)
        )
        print(f"查询到的作业数量: {homeworks.count()}")
        
        # 添加空数据检查
        if not course_nums:
            return JsonResponse({
                'error': '班级未关联任何课程',
                'debug': {
                    'student_class': class_num,
                    'course_nums': course_nums,
                    'homework_count': homeworks.count()
                }
            }, status=404)
        
        if homeworks.count() == 0:
            return JsonResponse({
                'error': '未找到课程对应的作业',
                'debug': {
                    'student_class': class_num,
                    'course_nums': course_nums,
                    'homework_count': homeworks.count()
                }
            }, status=404)
        serializer = HomeworkSerializer(homeworks, many=True)
        return JsonResponse({
            'debug': {
                'student_class': class_num,
                'course_nums': course_nums,
                'homework_count': homeworks.count()
            },
            'data': serializer.data
        }, safe=False)
    except Student.DoesNotExist:
        return JsonResponse({'error': '学生不存在'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)