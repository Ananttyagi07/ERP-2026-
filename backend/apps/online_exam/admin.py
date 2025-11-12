from django.contrib import admin
from .models import ExamInstruction, QuestionBank, OnlineExam, OnlineExamResult

@admin.register(ExamInstruction)
class ExamInstructionAdmin(admin.ModelAdmin):
    list_display = ['title', 'college', 'created_at']
    search_fields = ['title']

@admin.register(QuestionBank)
class QuestionBankAdmin(admin.ModelAdmin):
    list_display = ['subject', 'question_type', 'question_level', 'mark']
    search_fields = ['question']
    list_filter = ['question_type', 'question_level', 'subject']

@admin.register(OnlineExam)
class OnlineExamAdmin(admin.ModelAdmin):
    list_display = ['exam_title', 'subject', 'exam_date', 'publish_status']
    search_fields = ['exam_title']
    list_filter = ['publish_status', 'exam_date', 'subject']

@admin.register(OnlineExamResult)
class OnlineExamResultAdmin(admin.ModelAdmin):
    list_display = ['exam', 'student', 'obtained_mark', 'status', 'submitted_at']
    search_fields = ['student__user__first_name', 'student__user__last_name']
    list_filter = ['status', 'exam']
