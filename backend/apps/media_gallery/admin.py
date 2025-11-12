"""
Django admin configuration for media_gallery
"""
from django.contrib import admin
from .models import Gallery, GalleryImage


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_view_on_web']
    list_filter = ['created_at', 'is_view_on_web']
    search_fields = ['title', 'note']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['gallery', 'caption', 'image']
    list_filter = ['created_at']
    search_fields = ['caption']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


