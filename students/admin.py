from django.contrib import admin
from .models import Student, Submission

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 's_num')
    search_fields = ('name', 's_num')

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('u_num', 's_num', 'h_num', 'status', 'condition')
    search_fields = ('u_num', 's_num', 'h_num')
    readonly_fields = ('u_num',)
