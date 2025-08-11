from rest_framework import serializers
from .models import Teacher, Course, Class, CourseResource, Homework, CourseEnrollment

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['l_num', 'title', 't_num', 'des', 'type', 'credit', 'createtime', 'updatetime']
        read_only_fields = ['l_num', 'createtime', 'updatetime']

class TeacherSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(many=True, read_only=True)
    
    class Meta:
        model = Teacher
        fields = ['t_num', 'name', 'username', 'phone', 'email', 'createtime', 'courses']
        read_only_fields = ['t_num', 'createtime']

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['c_num', 'c_name', 't_num', 'grade', 'number', 'createtime', 'updatetime']
        read_only_fields = ['c_num', 'createtime', 'updatetime']

class CourseResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseResource
        fields = ['r_num', 'l_num', 'r_title', 'r_des', 'r_path', 'r_type', 'createtime']
        read_only_fields = ['r_num', 'createtime']

class HomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = ['h_num', 'l_num', 'title', 'des', 'hd_name', 'hd_path', 'hd_type', 'createtime', 'updatetime']
        read_only_fields = ['h_num', 'createtime', 'updatetime']

class CourseEnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseEnrollment
        fields = ['o_num', 'c_num', 'l_num', 'createtime']
        read_only_fields = ['o_num', 'createtime']