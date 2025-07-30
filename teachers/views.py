import os

import jwt
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from utils.middleware import ThreadLocalStorage
from .models import Teacher, Class, Course, CourseEnrollment, CourseResource
import utils.custom_jwt  # 假设已存在教师JWT序列化器
from django.db import transaction

from django.utils import timezone
import datetime
from students.models import Student  # 添加学生模型导入

from .models import Teacher, Class, Course, CourseEnrollment, Homework  # 更新导入

from utils.up_down_doc import upload_document  # 添加文件上传工具导入

# 教师登录验证
@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny])
def teacher_login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            teacher = Teacher.objects.get(username=username)

            if check_password(password, teacher.password):
                # 检查并创建User关联
                if not teacher.user:
                    user = User.objects.create_user(
                        username=teacher.username,
                        password=password
                    )
                    teacher.user = user
                    teacher.save()
                # 使用教师专用JWT序列化器生成令牌
                teacher.jwt = str(utils.custom_jwt.CustomTokenObtainPairSerializer.get_token(teacher))
                teacher.save()
                # 设置线程本地存储
                ThreadLocalStorage.set('user_type', 'teacher')
                ThreadLocalStorage.set('user_id', teacher.id)
                ThreadLocalStorage.set('user_num', teacher.t_num)
                ThreadLocalStorage.set('username', teacher.username)

                return Response({
                    'success': True,
                    'message': '登录成功',
                    'data': {
                        'jwt': teacher.jwt,
                        'username': teacher.username,
                        'name': teacher.name,
                        't_num': teacher.t_num
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'success': False,
                    'message': '密码错误'
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Teacher.DoesNotExist:
            return Response({
                'success': False,
                'message': '用户名不存在'
            }, status=status.HTTP_404_NOT_FOUND)

    return Response({
        'success': False,
        'message': '请使用POST方法'
    }, status=status.HTTP_405_METHOD_NOT_ALLOWED)

# 教师信息编辑
@api_view(['POST'])
@csrf_exempt
def teacher_edit(request):
    if request.method == 'POST':
        # 从线程存储获取当前用户ID
        id = ThreadLocalStorage.get('user_id')

        try:
            teacher = Teacher.objects.get(id=id)
        except Teacher.DoesNotExist:
            return Response({
                'success': False,
                'message': '用户未登录或会话已过期'
            }, status=status.HTTP_401_UNAUTHORIZED)

        # 定义教师可更新字段（不含class_num）
        updatable_fields = ['name', 'username', 'phone', 'email']

        # 遍历字段进行条件更新
        for field in updatable_fields:
            value = request.data.get(field)
            if value is not None and value != '':
                setattr(teacher, field, value)
        teacher.save()

        return Response({
            'success': True,
            'message': '信息更新成功',
            'data': {
                't_num': teacher.t_num,
                'name': teacher.name,
                'username': teacher.username,
                'phone': teacher.phone,
                'email': teacher.email
            }
        }, status=status.HTTP_200_OK)

    return Response({
        'success': False,
        'message': '请使用POST方法'
    }, status=status.HTTP_405_METHOD_NOT_ALLOWED)

# 教师密码修改
@api_view(['POST'])
@csrf_exempt
def teacher_change_password(request):
    if request.method == 'POST':
        # 从线程存储获取当前用户ID
        id = ThreadLocalStorage.get('user_id')
        # teacher = Teacher.objects.get(id=id)
        print(id)
        try:
            teacher = Teacher.objects.get(id=id)
        except Teacher.DoesNotExist:
            return Response({
                'success': False,
                'message': '用户未登录或会话已过期'
            }, status=status.HTTP_401_UNAUTHORIZED)

        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if check_password(old_password, teacher.password):
            teacher.password = make_password(new_password)
            teacher.save()
            return Response({
                'success': True,
                'message': '密码修改成功'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'success': False,
                'message': '原密码错误'
            }, status=status.HTTP_401_UNAUTHORIZED)

    return Response({
        'success': False,
        'message': '请使用POST方法'
    }, status=status.HTTP_405_METHOD_NOT_ALLOWED)

# 教师注册功能
@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny])
def teacher_register(request):
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
        if Teacher.objects.filter(username=username).exists() or User.objects.filter(username=username).exists():
            return Response({
                'success': False,
                'message': '用户名已存在'
            }, status=status.HTTP_400_BAD_REQUEST)
        try:
            # 创建Django User对象
            user = User.objects.create_user(
                username=username,
                password=password,
                email=request.data.get('email', '')
            )

            # 创建教师对象并关联User
            teacher = Teacher(
                user=user,  # 关联User
                username=username,
                password=make_password(password),  # 加密存储密码
                name=name,
                # 处理非必填字段
                phone=request.data.get('phone'),
                email=request.data.get('email')
                # t_num由系统自动生成，无需手动设置
            )
            teacher.save()
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'success': True,
            'message': '教师注册成功',
            'data': {
                'teacher_id': teacher.id,
                'username': teacher.username,
                'name': teacher.name,
                't_num': teacher.t_num  # 返回系统生成的工号
            }
        }, status=status.HTTP_201_CREATED)

    return Response({
        'success': False,
        'message': '请使用POST方法'
    }, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
@csrf_exempt
@transaction.atomic
def create_class(request):
    # 获取当前教师信息
    id = ThreadLocalStorage.get('user_id')
    teacher = Teacher.objects.get(id=id)
    if teacher is None:
        return Response({
            'status': 'error',
            'message': '教师信息获取失败'
        }, status=status.HTTP_400_BAD_REQUEST)

    # 获取请求数据
    c_name = request.data.get('c_name')
    grade = request.data.get('grade')
    number = request.data.get('number', 0)
    print(c_name, grade, number)
        # teacher = Teacher.objects.get(id=id)
    # 验证必填字段
    if not all([c_name]):
        return Response({
            'status': 'error',
            'message': '班级名称为必填字段'
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        with transaction.atomic():
            # 创建班级
            new_class = Class.objects.create(
                c_name=c_name,
                t_num=teacher.t_num,
                grade=grade,
                number=number
            )

            return Response({
                'status': 'success',
                'message': '班级创建成功',
                'data': {
                    'c_num': new_class.c_num,
                    'c_name': new_class.c_name,
                    'grade': new_class.grade,
                    'number': new_class.number
                }
            }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({
            'status': 'error',
            'message': '班级创建失败:'+str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@csrf_exempt
@transaction.atomic
def create_course(request):
    # 获取当前教师信息
    id = ThreadLocalStorage.get('user_id')
    try:
        teacher = Teacher.objects.get(id=id)
    except Teacher.DoesNotExist:
        return Response({
            'status': 'error',
            'message': '用户未登录或会话已过期'
        }, status=status.HTTP_401_UNAUTHORIZED)

    # 获取请求数据
    title = request.data.get('title')
    course_type = request.data.get('type')
    credit = request.data.get('credit')
    des = request.data.get('des', '')

    # 验证必填字段
    if not all([title, course_type, credit]):
        return Response({
            'status': 'error',
            'message': '课程名、课程类型和学分为必填字段'
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        # 创建课程
        course = Course.objects.create(
            title=title,
            t_num=teacher.t_num,
            des=des,
            type=course_type,
            credit=int(credit)
        )

        return Response({
            'status': 'success',
            'message': '课程创建成功',
            'data': {
                'l_num': course.l_num,
                'title': course.title,
                'type': course.type,
                'credit': course.credit,
                'createtime': course.createtime.strftime('%Y-%m-%d %H:%M:%S')
            }
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'课程创建失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@csrf_exempt
@transaction.atomic
def edit_class(request):
    # 获取当前教师信息
    id = ThreadLocalStorage.get('user_id')
    try:
        teacher = Teacher.objects.get(id=id)
    except Teacher.DoesNotExist:
        return Response({
            'status': 'error',
            'message': '用户未登录或会话已过期'
        }, status=status.HTTP_401_UNAUTHORIZED)

    # 获取请求数据
    c_num = request.data.get('c_num')
    c_name = request.data.get('c_name')
    grade = request.data.get('grade')
    number = request.data.get('number')

    # 验证必填字段
    if not c_num:
        return Response({
            'status': 'error',
            'message': '班级号为必填字段'
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        with transaction.atomic():
            # 查询班级并验证权限
            class_obj = Class.objects.get(c_num=c_num)
            if class_obj.t_num != teacher.t_num:
                return Response({
                    'status': 'error',
                    'message': '没有权限修改此班级信息'
                }, status=status.HTTP_403_FORBIDDEN)

            # 更新班级信息（仅允许修改指定字段）
                # 定义可更新字段
            updatable_fields = ['c_name', 'grade', 'number']
            updated = False

            # 更新课程信息
            for field in updatable_fields:
                value = request.data.get(field)
                if value is not None and value != getattr(class_obj, field):
                    setattr(class_obj, field, value)
                    updated = True
            # if c_name is not None:
            #     class_obj.c_name = c_name
            # if grade is not None:
            #     class_obj.grade = grade
            # if number is not None:
            #     class_obj.number = number
            class_obj.save()

            return Response({
                'status': 'success',
                'message': '班级信息更新成功',
                'data': {
                    'c_num': class_obj.c_num,
                    'c_name': class_obj.c_name,
                    'grade': class_obj.grade,
                    'number': class_obj.number,
                    't_num': class_obj.t_num
                }
            }, status=status.HTTP_200_OK)

    except Class.DoesNotExist:
        return Response({
            'status': 'error',
            'message': f'班级号{c_num}不存在'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'班级信息更新失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@csrf_exempt
@transaction.atomic
def edit_course(request):
    # 获取当前教师信息
    id = ThreadLocalStorage.get('user_id')
    try:
        teacher = Teacher.objects.get(id=id)
    except Teacher.DoesNotExist:
        return Response({
            'status': 'error',
            'message': '用户未登录或会话已过期'
        }, status=status.HTTP_401_UNAUTHORIZED)

    # 获取请求数据
    l_num = request.data.get('l_num')
    if not l_num:
        return Response({
            'status': 'error',
            'message': '课程号l_num为必填字段'
        }, status=status.HTTP_400_BAD_REQUEST)

    # 查询课程并验证权限
    try:
        course = Course.objects.get(l_num=l_num)
        # 验证当前教师是否为课程创建者
        if course.t_num != teacher.t_num:
            return Response({
                'status': 'error',
                'message': '无权限修改此课程'
            }, status=status.HTTP_403_FORBIDDEN)
    except Course.DoesNotExist:
        return Response({
            'status': 'error',
            'message': f'课程号为{l_num}的课程不存在'
        }, status=status.HTTP_404_NOT_FOUND)

    # 定义可更新字段
    updatable_fields = ['title', 'des', 'type', 'credit']
    updated = False

    # 更新课程信息
    for field in updatable_fields:
        value = request.data.get(field)
        if value is not None and value != getattr(course, field):
            setattr(course, field, value)
            updated = True

    if updated:
        course.save()
        return Response({
            'status': 'success',
            'message': '课程信息更新成功',
            'data': {
                'l_num': course.l_num,
                'title': course.title,
                'type': course.type,
                'credit': course.credit,
                'des': course.des,
                'updatetime': course.updatetime.strftime('%Y-%m-%d %H:%M:%S')
            }
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            'status': 'success',
            'message': '未检测到需要更新的课程信息',
            'data': {
                'l_num': course.l_num,
                'title': course.title
            }
        }, status=status.HTTP_200_OK)


@api_view(['POST'])
@csrf_exempt
@transaction.atomic
def enroll_course(request):
    # 获取当前教师信息
    id = ThreadLocalStorage.get('user_id')
    try:
        teacher = Teacher.objects.get(id=id)
    except Teacher.DoesNotExist:
        return Response({
            'status': 'error',
            'message': '用户未登录或会话已过期'
        }, status=status.HTTP_401_UNAUTHORIZED)

    # 获取请求数据
    c_num = request.data.get('c_num')
    l_num = request.data.get('l_num')

    # 验证必填字段
    if not all([c_num, l_num]):
        return Response({
            'status': 'error',
            'message': '班级号和课程号为必填字段'
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        with transaction.atomic():
            # 验证班级是否存在且属于当前教师
            class_obj = Class.objects.get(c_num=c_num)
            if class_obj.t_num != teacher.t_num:
                return Response({
                    'status': 'error',
                    'message': '没有权限操作此班级'
                }, status=status.HTTP_403_FORBIDDEN)

            # 验证课程是否存在且属于当前教师
            course_obj = Course.objects.get(l_num=l_num)
            if course_obj.t_num != teacher.t_num:
                return Response({
                    'status': 'error',
                    'message': '没有权限操作此课程'
                }, status=status.HTTP_403_FORBIDDEN)

            # 创建选修记录
            enrollment = CourseEnrollment.objects.create(
                c_num=c_num,
                l_num=l_num
            )

            return Response({
                'status': 'success',
                'message': '班级选修课程成功',
                'data': {
                    'o_num': enrollment.o_num,
                    'c_num': enrollment.c_num,
                    'l_num': enrollment.l_num,
                    'class_name': class_obj.c_name,
                    'course_name': course_obj.title,
                    'createtime': enrollment.createtime.strftime('%Y-%m-%d %H:%M:%S')
                }
            }, status=status.HTTP_201_CREATED)

    except Class.DoesNotExist:
        return Response({
            'status': 'error',
            'message': f'班级号{c_num}不存在'
        }, status=status.HTTP_404_NOT_FOUND)
    except Course.DoesNotExist:
        return Response({
            'status': 'error',
            'message': f'课程号{l_num}不存在'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'选修操作失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@csrf_exempt
def update_student_class(request):
    if request.method == 'POST':
        # 获取当前教师工号
        t_id = ThreadLocalStorage.get('user_id')
        teacher = Teacher.objects.get(id=t_id)
        t_num = teacher.t_num
        if not t_num:
            return Response({
                'success': False,
                'message': '用户未登录或会话已过期'
            }, status=status.HTTP_401_UNAUTHORIZED)
            
        # 获取请求参数
        s_num = request.data.get('s_num')
        c_num = request.data.get('c_num')
        
        # 参数验证
        if not all([s_num, c_num]):
            return Response({
                'success': False,
                'message': '学生学号和班级号为必填项'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        # 验证班级是否属于当前教师
        try:
            class_obj = Class.objects.get(c_num=c_num, t_num=t_num)
        except Class.DoesNotExist:
            return Response({
                'success': False,
                'message': '无权限修改该班级学生'
            }, status=status.HTTP_403_FORBIDDEN)
            
        # 更新学生班级
        try:
            student = Student.objects.get(s_num=s_num)
            student.class_num = c_num
            student.save()
            
            return Response({
                'success': True,
                'message': '学生班级更新成功',
                'data': {
                    's_num': student.s_num,
                    'name': student.name,
                    'class_num': student.class_num
                }
            }, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            return Response({
                'success': False,
                'message': '学生不存在'
            }, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@csrf_exempt
def update_students_class_batch(request):
    if request.method == 'POST':
        # 获取当前教师工号
        t_id = ThreadLocalStorage.get('user_id')
        teacher = Teacher.objects.get(id=t_id)
        t_num = teacher.t_num
        if not t_num:
            return Response({
                'success': False,
                'message': '用户未登录或会话已过期'
            }, status=status.HTTP_401_UNAUTHORIZED)
            
        # 获取请求参数
        s_num_list = request.data.get('s_num_list')  # 学生号列表
        c_num = request.data.get('c_num')  # 目标班级号
        
        # 参数验证
        if not all([s_num_list, c_num]) or not isinstance(s_num_list, list):
            return Response({
                'success': False,
                'message': '学生学号列表和班级号为必填项，且学生学号必须为列表格式'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        # 验证班级是否属于当前教师
        try:
            class_obj = Class.objects.get(c_num=c_num, t_num=t_num)
        except Class.DoesNotExist:
            return Response({
                'success': False,
                'message': '无权限修改该班级学生'
            }, status=status.HTTP_403_FORBIDDEN)
            
        # 查询所有存在的学生
        existing_students = Student.objects.filter(s_num__in=s_num_list)
        existing_s_nums = [student.s_num for student in existing_students]
        non_existing_s_nums = list(set(s_num_list) - set(existing_s_nums))
        
        # 批量更新学生班级
        if existing_students.exists():
            existing_students.update(class_num=c_num)
            
            # 准备返回数据
            updated_students = existing_students.values('s_num', 'name', 'class_num')
            result = {
                'success': True,
                'message': f'成功更新{len(existing_students)}名学生的班级信息',
                'data': {
                    'updated_students': list(updated_students),
                    'non_existing_students': non_existing_s_nums
                }
            }
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response({
                'success': False,
                'message': '未找到任何有效学生',
                'data': {
                    'non_existing_students': non_existing_s_nums
                }
            }, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@csrf_exempt
@transaction.atomic
def create_homework(request):
    if request.method == 'POST':
        # 获取当前教师工号
        t_id = ThreadLocalStorage.get('user_id')
        teacher = Teacher.objects.get(id=t_id)
        t_num = teacher.t_num
        if not t_num:
            return Response({
                'success': False,
                'message': '用户未登录或会话已过期'
            }, status=status.HTTP_401_UNAUTHORIZED)
            
        # 获取请求参数
        l_num = request.data.get('l_num')  # 课程号
        title = request.data.get('title')  # 作业标题
        des = request.data.get('des', '')  # 作业说明
        
        # 获取上传文件
        homework_file = request.FILES.get('file')  # 从FILES获取文件对象
        
        # 参数验证
        if not all([l_num, title]):
            return Response({
                'success': False,
                'message': '课程号和作业标题为必填项'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        # 验证课程是否属于当前教师
        try:
            course = Course.objects.get(l_num=l_num, t_num=t_num)
        except Course.DoesNotExist:
            return Response({
                'success': False,
                'message': '无权限操作此课程或课程不存在'
            }, status=status.HTTP_403_FORBIDDEN)
            
        # 文件上传处理
        hd_path = ''
        hd_name = ''
        hd_type = ''
        
        if homework_file:
            # 定义文件上传参数
            save_dir = 'media\\homework_files'  # 文件保存目录
            allowed_types = ['.pdf', '.docx', '.doc', '.txt', '.zip', '.rar']  # 允许的文件类型
            hd_name = homework_file.name  # 原始文件名
            hd_type = os.path.splitext(hd_name)[1].lower()  # 文件类型
            
            # 调用文件上传工具
            upload_result = upload_document(
                file=homework_file,
                save_dir=save_dir,
                filename=hd_name,
                allowed_types=allowed_types
            )
            
            # 检查上传结果
            if not upload_result['success']:
                return Response({
                    'success': False,
                    'message': upload_result['message']
                }, status=status.HTTP_400_BAD_REQUEST)
            hd_path = upload_result['path']  # 获取上传后的文件路径
        
        # 创建作业记录
        try:
            homework = Homework(
                l_num=l_num,
                title=title,
                des=des,
                hd_name=hd_name,
                hd_path=hd_path,
                hd_type=hd_type
            )
            homework.save()
            
            return Response({
                'success': True,
                'message': '作业发布成功',
                'data': {
                    'h_num': homework.h_num,
                    'l_num': homework.l_num,
                    'title': homework.title,
                    'hd_name': homework.hd_name,
                    'hd_path': homework.hd_path,
                    'hd_type': homework.hd_type,
                    'createtime': homework.createtime.strftime('%Y-%m-%d %H:%M:%S')
                }
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                'success': False,
                'message': f'作业创建失败: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
@csrf_exempt
@transaction.atomic
def upload_course_resource(request):
    # 获取当前教师信息
    id = ThreadLocalStorage.get('user_id')
    try:
        teacher = Teacher.objects.get(id=id)
    except Teacher.DoesNotExist:
        return Response({
            'success': False,
            'message': '用户未登录或会话已过期'
        }, status=status.HTTP_401_UNAUTHORIZED)

    # 验证请求参数
    l_num = request.data.get('l_num')
    r_title = request.data.get('r_title')
    r_des = request.data.get('r_des', '')
    file = request.FILES.get('file')

    if not all([l_num, r_title, file]):
        return Response({
            'success': False,
            'message': '课程号、资源标题和文件为必填项'
        }, status=status.HTTP_400_BAD_REQUEST)

    # 验证课程归属权
    try:
        course = Course.objects.get(l_num=l_num)
        if course.t_num != teacher.t_num:
            return Response({
                'success': False,
                'message': '无权限操作此课程资源'
            }, status=status.HTTP_403_FORBIDDEN)
    except Course.DoesNotExist:
        return Response({
            'success': False,
            'message': '课程不存在'
        }, status=status.HTTP_404_NOT_FOUND)

    # 处理文件上传
    save_dir = 'media\\course_resources'
    filename = file.name
    allowed_types = ['.pdf', '.doc', '.docx', '.ppt', '.pptx', '.xls', '.xlsx', '.zip', '.rar']

    upload_result = upload_document(file, save_dir, filename, allowed_types)
    if not upload_result['success']:
        return Response({
            'success': False,
            'message': upload_result['message']
        }, status=status.HTTP_400_BAD_REQUEST)

    # 创建课程资源记录
    resource = CourseResource(
        l_num=l_num,
        r_title=r_title,
        r_des=r_des,
        r_path=upload_result['path'],
        r_type=filename.split('.')[-1].lower() if '.' in filename else ''
    )
    resource.save()

    return Response({
        'success': True,
        'message': '课程资源上传成功',
        'data': {
            'r_num': resource.r_num,
            'l_num': resource.l_num,
            'r_title': resource.r_title,
            'r_des': resource.r_des,
            'r_path': resource.r_path,
            'r_type': resource.r_type,
            'createtime': resource.createtime
        }
    }, status=status.HTTP_201_CREATED)