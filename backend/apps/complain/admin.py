"""
Django admin configuration for complain
"""
from django.contrib import admin
from .models import ComplainType, Complain


@admin.register(ComplainType)
class ComplainTypeAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['created_at']
    search_fields = ['name']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


@admin.register(Complain)
class ComplainAdmin(admin.ModelAdmin):
    list_display = ['complain_type', 'user_type', 'complain_date']
    list_filter = ['created_at', 'user_type', 'complain_date']
    search_fields = ['complain_text']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


