from django.urls import path
from . import views
urlpatterns = [
    path('login/', views.teacher_login, name='login'),
    path('editinfo/', views.teacher_edit, name='editinfo'),
    path('editpwd/', views.teacher_change_password, name='editpwd'),
    path('register/', views.teacher_register, name='register'),
    path('createcourse/', views.create_course, name='teacher_create_course'),
    path('createclass/', views.create_class, name='teacher_create_class'),
    path('editcourse/', views.edit_course, name='teacher_edit_course'),
    path('editclass/', views.edit_class, name='edit_class'),
    path('enrollcourse/', views.enroll_course, name='enroll_course'),
    path('updatestudentclass/', views.update_student_class, name='updatestudentclass'),  # 原有路由
    path('updatestudentsclassbatch/', views.update_students_class_batch, name='updatestudentsclassbatch'),  # 批量更新路由
    path('createhomework/', views.create_homework, name='create_homework'),  # 新增作业发布路由
    path('uploadresource/', views.upload_course_resource, name='teacher_upload_resource'),  # 新增资源上传路由
]