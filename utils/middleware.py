import threading
from datetime import datetime

from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework_simplejwt.backends import TokenBackend
from django.conf import settings
from rest_framework_simplejwt.exceptions import TokenError

from students.models import Student
from teachers.models import Teacher


class ThreadLocalStorage:
    _local = threading.local()

    @classmethod
    def set(cls, key, value):
        setattr(cls._local, key, value)

    @classmethod
    def get(cls, key, default=None):
        return getattr(cls._local, key, default)

    @classmethod
    def delete(cls, key):
        if hasattr(cls._local, key):
            delattr(cls._local, key)

    @classmethod
    def clear(cls):
        cls._local.__dict__.clear()

import jwt
from django.conf import settings
from rest_framework import exceptions, status


class UserContextMiddleware(MiddlewareMixin):
    def process_request(self, request):
        EXCLUDED_PATHS = [
            '/students/login/',
            '/students/register/',
            '/teachers/login/',
            '/teachers/register/',
        ]
        # 清除之前的上下文
        ThreadLocalStorage.clear()
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        # auth_header= auth_header.split(' ')[1]
        if auth_header:
            try:
                # auth_header.verify()
                payload = jwt.decode(str(auth_header), settings.SECRET_KEY, algorithms=['HS256'],verify=True)
                exptime = payload['exp']
                if datetime.utcnow() >datetime.fromtimestamp(exptime):
                    return JsonResponse({'error': 'Token expired'})
                id=payload.get('user_id')
                usertype=payload.get('user_type')
                if usertype == 'student':
                    user1 = Student.objects.get(id=id)
                    if user1.jwt!=auth_header:
                        return JsonResponse({'success': False,
                    'message': '令牌已失效请重新登录'}, status=status.HTTP_403_FORBIDDEN)
                elif usertype == 'teacher':
                    user1 = Teacher.objects.get(id=id)
                    if user1.jwt!=auth_header:
                        return JsonResponse({'success': False,
                    'message': '令牌已失效请重新登录'}, status=status.HTTP_403_FORBIDDEN)
                if usertype == 'student':
                    # student = request.user.student
                    # print(request.user)
                    # print(student)
                    # print(student.id)
                    # print(student.s_num)
                    # print(request.user.username)
                    print('student')
                    ThreadLocalStorage.set('user_type', 'student')
                    ThreadLocalStorage.set('user_id', id)
                    # ThreadLocalStorage.set('user_num', student.s_num)
                    # ThreadLocalStorage.set('username', request.user.username)
                # 教师用户
                elif usertype == 'teacher':
                    # teacher = request.user.teacher
                    # print(teacher)
                    print('teacher')
                    ThreadLocalStorage.set('user_type', 'teacher')
                    ThreadLocalStorage.set('user_id', id)
                    # ThreadLocalStorage.set('user_num', teacher.t_num)
                    # ThreadLocalStorage.set('username', request.user.username)
            except TokenError as e:
                return JsonResponse({'status': 'error',
                    'message': str(e)}, status=status.HTTP_403_FORBIDDEN)
            print('过')

        # 支持JWT和会话认证两种方式
        # if hasattr(request, 'user') and request.user.is_authenticated:
        #     try:
        #          # 手动解析JWT令牌获取用户
        #         auth_header = request.META.get('HTTP_AUTHORIZATION')
        #         print(request.META)
        #         print(auth_header)
        #         # if auth_header and auth_header.startswith('Bearer '):
        #         if auth_header :
        #             token = auth_header.split('.')[1]
        #             print('1')
        #             try:
        #                 token_backend = TokenBackend(
        #                     algorithm='HS256',
        #                     signing_key=settings.SECRET_KEY
        #                     # options={'verify_exp': True}
        #                 )
        #                 payload = token_backend.decode(auth_header, verify=True)
        #                 print('1.5')
        #                 print(payload)
        #                 user_id = payload.get('user_id')
        #                 username = payload.get('username')
        #                 num = payload.get('num')
        #                 user = User.objects.get(id=user_id)
        #                 # ThreadLocalStorage.set('user', user)
        #                 # ThreadLocalStorage.set('user_type', 'student')
        #                 ThreadLocalStorage.set('user_id', user_id)
        #                 ThreadLocalStorage.set('num', num)
        #                 ThreadLocalStorage.set('username', username)
        #                 print('2')
        #                 print(user_id,username,num)
        #             except Exception as e:
        #                 # 处理令牌无效/过期等异常
        #                 print(f"JWT解析失败: {str(e)}")

        
       

    def process_response(self, request, response):
        # 线程本地存储自动清理（无需依赖请求结束）
        ThreadLocalStorage.clear()
        return response

    def process_exception(self, request, exception):
        ThreadLocalStorage.clear()