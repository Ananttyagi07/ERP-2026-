from django.contrib import admin
from .models import Grade, ExamTerm, ExamSchedule, ExamSuggestion, ExamAttendanceRecord

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['grade_name', 'point', 'mark_from', 'mark_to']
    search_fields = ['grade_name']

@admin.register(ExamTerm)
class ExamTermAdmin(admin.ModelAdmin):
    list_display = ['name', 'college', 'created_at']
    search_fields = ['name']

@admin.register(ExamSchedule)
class ExamScheduleAdmin(admin.ModelAdmin):
    list_display = ['exam_term', 'subject', 'school_class', 'exam_date', 'exam_time']
    search_fields = ['subject__name']
    list_filter = ['exam_term', 'school_class', 'exam_date']

@admin.register(ExamSuggestion)
class ExamSuggestionAdmin(admin.ModelAdmin):
    list_display = ['title', 'exam_term', 'subject', 'school_class']
    search_fields = ['title']
    list_filter = ['exam_term', 'subject']

@admin.register(ExamAttendanceRecord)
class ExamAttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ['exam_schedule', 'student', 'status']
    search_fields = ['student__user__first_name', 'student__user__last_name']
    list_filter = ['status', 'exam_schedule']
