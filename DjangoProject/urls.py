"""
URL configuration for DjangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from goods import views as goods_views

urlpatterns = [
    path("admin/", admin.site.urls),
    # path("index/", views.index),
    # path("calculate/", views.calculate),
    #
    # path("cal/", views.cal),

    # path('firstweb/',include('firstwWEB.urls')),

    path('api/',include('api.urls')),

    path('studentlist/',goods_views.studentlist),

    path('studentadd/', goods_views.addstudent),

    path('updatestudent/', goods_views.updatestudent),

    path('deletestudent/<int:sid>', goods_views.deletestudent),

    path('upload_document/', goods_views.upload_document),

    path('download_document/', goods_views.download_document,name='download_document'),

    path('adddocument/', goods_views.add_document),

    path('login_student/', goods_views.login_student,name='login'),
    path('student_dashboard/', goods_views.student_dashboard),

    path('student_submissions/', goods_views.student_submissions, name='student_submissions'),
    # 新增学生和教师应用路由
    path('students/', include('students.urls')),
    path('teachers/', include('teachers.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
