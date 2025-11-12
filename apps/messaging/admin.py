"""
Django admin configuration for messaging
"""
from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'subject', 'is_read', 'is_draft']
    list_filter = ['created_at']
    search_fields = ['sender', 'receiver', 'subject']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


