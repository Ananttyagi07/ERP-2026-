"""
Django admin configuration for event
"""
from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_for', 'from_date', 'to_date', 'is_view_on_web']
    list_filter = ['created_at', 'event_for', 'from_date']
    search_fields = ['title', 'event_place']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


