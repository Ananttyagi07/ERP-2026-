"""
Django admin configuration for frontend_cms
"""
from django.contrib import admin
from .models import FrontendPage, Slider, AboutSchool


@admin.register(FrontendPage)
class FrontendPageAdmin(admin.ModelAdmin):
    list_display = ['location', 'title', 'url_slug']
    list_filter = ['created_at', 'location']
    search_fields = ['title', 'url_slug']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ['caption', 'image']
    list_filter = ['created_at']
    search_fields = ['caption']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


@admin.register(AboutSchool)
class AboutSchoolAdmin(admin.ModelAdmin):
    list_display = ['content', 'image']
    list_filter = ['created_at']
    search_fields = ['content']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


