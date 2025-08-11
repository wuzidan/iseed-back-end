from django.urls import path
from . import views
urlpatterns = [
    path('login/', views.teacher_login, name='login'),
    path('editinfo/', views.teacher_edit, name='editinfo'),# 修改教师个人信息
    path('editpwd/', views.teacher_change_password, name='editpwd'),
    path('register/', views.teacher_register, name='register'),
    path('profile/<str:t_num>/', views.get_teacher_profile, name='get_teacher_profile'),# 获取教师个人信息
    path('createcourse/', views.create_course, name='teacher_create_course'),
    path('createclass/', views.create_class, name='teacher_create_class'),
    path('editcourse/', views.edit_course, name='teacher_edit_course'),# 修改课程信息
    path('editclass/', views.edit_class, name='edit_class'),
    path('enrollcourse/', views.enroll_course, name='enroll_course'),
    path('updatestudentclass/', views.update_student_class, name='updatestudentclass'),  # 原有路由
    path('updatestudentsclassbatch/', views.update_students_class_batch, name='updatestudentsclassbatch'),  # 批量更新路由
    path('createhomework/', views.create_homework, name='create_homework'),  # 新增作业发布路由
    path('uploadresource/', views.upload_course_resource, name='teacher_upload_resource'),  # 新增资源上传路由
    path('mycourses/', views.get_teacher_courses, name='get_teacher_courses'),# 获取当前教师的课程列表
    path('courses/<str:l_num>/', views.get_course, name='get_course'),# 获取指定课程的详细信息(l_num为课程号) 
    path('homeworks/', views.get_homeworks, name='get_homeworks'),# 获取所有作业列表
    path('homeworks/<str:h_num>/', views.get_homework, name='get_homework'),# 获取指定作业的详细信息(h_num为作业号)
]