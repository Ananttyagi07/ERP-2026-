"""Live Classes admin"""
from django.contrib import admin
from .models import LiveClassType, LiveClass, Assignment

@admin.register(LiveClassType)
class LiveClassTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at']
    search_fields = ['name']

@admin.register(LiveClass)
class LiveClassAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'teacher', 'class_date', 'start_time', 'status']
    search_fields = ['subject__name']
    list_filter = ['status', 'class_date']

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'school_class', 'section', 'subject', 'submission_date', 'status']
    search_fields = ['title']
    list_filter = ['status', 'assignment_date']
