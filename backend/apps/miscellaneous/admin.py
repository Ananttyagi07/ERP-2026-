"""
Django admin configuration for miscellaneous
"""
from django.contrib import admin
from .models import Award, Todo, FAQ


@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = ['user_type', 'title', 'gift', 'date']
    list_filter = ['created_at', 'user_type', 'date']
    search_fields = ['title', 'gift']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'work_status', 'user_type']
    list_filter = ['created_at', 'work_status', 'user_type']
    search_fields = ['title', 'description']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['title', 'description']
    list_filter = ['created_at']
    search_fields = ['title', 'description']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


