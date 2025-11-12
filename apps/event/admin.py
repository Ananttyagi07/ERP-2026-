"""
Django admin configuration for event
"""
from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_from', 'event_to', 'is_view_on_web']
    list_filter = ['created_at']
    search_fields = ['title', 'event_from', 'event_to']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


