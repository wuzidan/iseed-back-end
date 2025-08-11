from django.contrib import admin
from .models import Teacher, Course, Homework, Class, CourseEnrollment

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 't_num', 'email')
    search_fields = ('name', 't_num', 'email')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'teacher', 'l_num', 'credit')
    fields = ('title', 'teacher', 'des', 'type', 'credit')
    search_fields = ('title', 'l_num', 't_num')

@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'l_num', 'h_num')
    fields = ('title', 'des', 'course', 'hd_name', 'hd_path', 'hd_type')
    search_fields = ('title', 'h_num', 'l_num')

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('id', 'c_num', 'c_name', 'grade')
    fields = ('c_num', 'c_name', 'grade', 'number')
    search_fields = ('c_num', 'name', 'l_num')

@admin.register(CourseEnrollment)
class CourseEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'o_num', 'c_num', 'l_num')
    fields = ('c_num', 'l_num')
    search_fields = ('c_num', 'l_num')

# Register your models here.
