"""
Django admin configuration for communication
"""
from django.contrib import admin
from .models import EmailLog, SMSLog


@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ['receiver_type', 'subject', 'sent_at']
    list_filter = ['created_at']
    search_fields = ['receiver_type', 'subject', 'sent_at']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


@admin.register(SMSLog)
class SMSLogAdmin(admin.ModelAdmin):
    list_display = ['message', 'gateway', 'sent_at']
    list_filter = ['created_at']
    search_fields = ['message', 'gateway', 'sent_at']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


