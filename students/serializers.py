from rest_framework import serializers
from .models import Submission,Student
from goods.models import DocumentSubmission
from teachers.models import Course, Homework, CourseResource

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'  # 自动包含所有字段

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['s_num', 'name', 'username', 'class_num', 'phone', 'email', 'createtime']
        read_only_fields = ['s_num', 'createtime']

class CourseResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseResource
        fields = ['r_num', 'r_title', 'r_des', 'r_path', 'r_type', 'createtime']

class HomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = ['h_num', 'title', 'des', 'hd_name', 'hd_path', 'hd_type', 'createtime']

class CourseSerializer(serializers.ModelSerializer):
    homeworks = serializers.SerializerMethodField()
    resources = CourseResourceSerializer(many=True, read_only=True)
    
    class Meta:
        model = Course
        fields = ['l_num', 'title', 'des', 'type', 'credit', 'createtime', 'homeworks', 'resources']
    
    def get_homeworks(self, obj):
        homeworks = Homework.objects.filter(l_num=obj.l_num)
        return HomeworkSerializer(homeworks, many=True).data

class DocumentSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentSubmission
        fields = ['u_num', 's_num', 't_num', 'up_time', 'status', 'score', 'filename', 'path']