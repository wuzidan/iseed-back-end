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
            class_name=request.data.get('class_name'),
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
