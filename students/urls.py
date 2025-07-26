from django.urls import path
from . import views
urlpatterns = [
    path('login/', views.student_login, name='login'),
    path('editinfo/', views.student_edit, name='editinfo'),
    path('editpwd/', views.student_change_password, name='editpwd'),
    path('register/', views.student_register, name='register'),
]