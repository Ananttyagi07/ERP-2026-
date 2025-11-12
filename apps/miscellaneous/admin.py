"""
Django admin configuration for miscellaneous
"""
from django.contrib import admin
from .models import Award, Todo, FAQ


@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = ['award_to_type', 'award_name', 'gift', 'date']
    list_filter = ['created_at']
    search_fields = ['award_to_type', 'award_name', 'gift']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'status', 'is_completed']
    list_filter = ['created_at']
    search_fields = ['title', 'date', 'status']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer', 'is_active']
    list_filter = ['created_at']
    search_fields = ['question', 'answer', 'is_active']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


