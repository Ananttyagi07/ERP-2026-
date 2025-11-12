"""
Django admin configuration for complain
"""
from django.contrib import admin
from .models import ComplainType, Complain


@admin.register(ComplainType)
class ComplainTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


@admin.register(Complain)
class ComplainAdmin(admin.ModelAdmin):
    list_display = ['complain_type', 'complain_by_type', 'subject', 'date']
    list_filter = ['created_at']
    search_fields = ['complain_type', 'complain_by_type', 'subject']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


