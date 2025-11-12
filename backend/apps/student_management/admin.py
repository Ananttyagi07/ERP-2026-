from django.contrib import admin
from .models import StudentType, OnlineAdmission, StudentActivity

@admin.register(StudentType)
class StudentTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'college', 'created_at']
    search_fields = ['name']
    list_filter = ['college', 'created_at']

@admin.register(OnlineAdmission)
class OnlineAdmissionAdmin(admin.ModelAdmin):
    list_display = ['student_name', 'email', 'phone', 'school_class', 'status', 'created_at']
    search_fields = ['student_name', 'email', 'phone']
    list_filter = ['status', 'school_class', 'created_at']

@admin.register(StudentActivity)
class StudentActivityAdmin(admin.ModelAdmin):
    list_display = ['student', 'school_class', 'section', 'activity_date']
    search_fields = ['student__user__first_name', 'student__user__last_name']
    list_filter = ['school_class', 'section', 'activity_date']
