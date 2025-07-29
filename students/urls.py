from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.student_login, name='login'),
    path('editinfo/', views.student_edit, name='editinfo'),
    path('editpwd/', views.student_change_password, name='editpwd'),
    path('register/', views.student_register, name='register'),
    path('uploadhomework/', views.upload_homework, name='upload_homework'),
    path('get_submission_record/', views.get_submission_record, name='get_submission_record'),
    path('get_submission_document/', views.get_submission_document, name='get_submission_document'),
]