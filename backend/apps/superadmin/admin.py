"""Superadmin admin"""
from django.contrib import admin
from .models import SuperAdminProfile

@admin.register(SuperAdminProfile)
class SuperAdminProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'national_id', 'birth_date', 'created_at']
    search_fields = ['user__email', 'user__username', 'national_id']
    list_filter = ['blood_group', 'religion', 'created_at']
