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
from .models import Teacher, Class, Course, CourseEnrollment
import utils.custom_jwt  # 假设已存在教师JWT序列化器
from django.db import transaction

from django.utils import timezone
import datetime

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

