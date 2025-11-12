"""
Django admin configuration for announcement
"""
from django.contrib import admin
from .models import Notice, News, Holiday


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'notice_for', 'is_view_on_web']
    list_filter = ['created_at', 'notice_for', 'date']
    search_fields = ['title']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'is_view_on_web']
    list_filter = ['created_at', 'date']
    search_fields = ['title', 'news_text']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ['title', 'from_date', 'to_date', 'is_view_on_web']
    list_filter = ['created_at']
    search_fields = ['title', 'from_date', 'to_date']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


