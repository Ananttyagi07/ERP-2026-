from django.contrib import admin
from .models import (
    StudentAttendance, TeacherAttendance, EmployeeAttendance,
    AbsentEmailLog, AbsentSMSLog
)

@admin.register(StudentAttendance)
class StudentAttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'school_class', 'section', 'attendance_date', 'status']
    search_fields = ['student__user__first_name', 'student__user__last_name']
    list_filter = ['status', 'attendance_date', 'school_class']

@admin.register(TeacherAttendance)
class TeacherAttendanceAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'attendance_date', 'status']
    search_fields = ['teacher__user__first_name', 'teacher__user__last_name']
    list_filter = ['status', 'attendance_date']

@admin.register(EmployeeAttendance)
class EmployeeAttendanceAdmin(admin.ModelAdmin):
    list_display = ['employee', 'attendance_date', 'status']
    search_fields = ['employee__user__first_name', 'employee__user__last_name']
    list_filter = ['status', 'attendance_date']

@admin.register(AbsentEmailLog)
class AbsentEmailLogAdmin(admin.ModelAdmin):
    list_display = ['receiver_type', 'receiver_email', 'absent_date', 'created_at']
    search_fields = ['receiver_email']
    list_filter = ['receiver_type', 'absent_date']

@admin.register(AbsentSMSLog)
class AbsentSMSLogAdmin(admin.ModelAdmin):
    list_display = ['receiver_type', 'receiver_phone', 'absent_date', 'created_at']
    search_fields = ['receiver_phone']
    list_filter = ['receiver_type', 'absent_date']
