from django.urls import path
from . import views

urlpatterns = [
    path('courses/', views.get_courses, name='get_courses'),
    path('login/', views.student_login, name='login'),
    path('editinfo/', views.student_edit, name='editinfo'),
    path('editpwd/', views.student_change_password, name='editpwd'),
    path('register/', views.student_register, name='register'),
    path('uploadhomework/', views.upload_homework, name='upload_homework'),
    path('submission-records/', views.get_submission_records, name='get_submission_records'),
    path('get_submission_document/', views.get_submission_document, name='get_submission_document'),
    path('get_student_info/<str:s_num>/', views.get_student_info, name='get_student_info'),# 获取学生个人信息
    path('info/update/<str:s_num>/', views.update_student_info, name='update_student_info'),# 更新学生个人信息
    path('courses/<str:s_num>/', views.get_student_courses, name='get_student_courses'),# 获取学生课程信息
    path('homeworks/<str:s_num>/', views.get_student_homeworks, name='get_student_homeworks'),# 获取学生作业信息

]