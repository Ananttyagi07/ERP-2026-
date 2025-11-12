from django.contrib import admin
from .models import (
    ExamMark, MarkDistribution, ResultCard,
    MarkEmailLog, MarkSMSLog, ResultEmailLog, ResultSMSLog
)

@admin.register(ExamMark)
class ExamMarkAdmin(admin.ModelAdmin):
    list_display = ['student', 'exam_schedule', 'total_mark', 'grade', 'attendance_status']
    search_fields = ['student__user__first_name', 'student__user__last_name']
    list_filter = ['exam_schedule', 'attendance_status']

@admin.register(MarkDistribution)
class MarkDistributionAdmin(admin.ModelAdmin):
    list_display = ['exam_term', 'school_class', 'subject']
    list_filter = ['exam_term', 'school_class', 'subject']

@admin.register(ResultCard)
class ResultCardAdmin(admin.ModelAdmin):
    list_display = ['student', 'exam_term', 'obtained_marks', 'percentage', 'result_status', 'merit_position']
    search_fields = ['student__user__first_name', 'student__user__last_name']
    list_filter = ['exam_term', 'result_status']

@admin.register(MarkEmailLog)
class MarkEmailLogAdmin(admin.ModelAdmin):
    list_display = ['student', 'receiver_email', 'exam_schedule', 'created_at']
    search_fields = ['receiver_email']

@admin.register(MarkSMSLog)
class MarkSMSLogAdmin(admin.ModelAdmin):
    list_display = ['student', 'receiver_phone', 'exam_schedule', 'created_at']
    search_fields = ['receiver_phone']

@admin.register(ResultEmailLog)
class ResultEmailLogAdmin(admin.ModelAdmin):
    list_display = ['student', 'receiver_email', 'exam_term', 'created_at']
    search_fields = ['receiver_email']

@admin.register(ResultSMSLog)
class ResultSMSLogAdmin(admin.ModelAdmin):
    list_display = ['student', 'receiver_phone', 'exam_term', 'created_at']
    search_fields = ['receiver_phone']
