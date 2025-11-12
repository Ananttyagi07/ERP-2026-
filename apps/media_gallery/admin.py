"""
Django admin configuration for media_gallery
"""
from django.contrib import admin
from .models import Gallery, GalleryImage


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'is_view_on_web']
    list_filter = ['created_at']
    search_fields = ['title', 'description', 'is_view_on_web']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['gallery', 'title', 'image']
    list_filter = ['created_at']
    search_fields = ['gallery', 'title', 'image']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


