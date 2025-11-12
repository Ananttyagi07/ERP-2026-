"""
Django admin configuration for frontend_cms
"""
from django.contrib import admin
from .models import FrontendPage, Slider, AboutSchool


@admin.register(FrontendPage)
class FrontendPageAdmin(admin.ModelAdmin):
    list_display = ['page_title', 'page_slug', 'is_active']
    list_filter = ['created_at']
    search_fields = ['page_title', 'page_slug', 'is_active']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active']
    list_filter = ['created_at']
    search_fields = ['title', 'is_active']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


@admin.register(AboutSchool)
class AboutSchoolAdmin(admin.ModelAdmin):
    list_display = ['title', 'description']
    list_filter = ['created_at']
    search_fields = ['title', 'description']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


