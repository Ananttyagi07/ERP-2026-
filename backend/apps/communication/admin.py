"""
Django admin configuration for communication
"""
from django.contrib import admin
from .models import EmailLog, SMSLog


@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ['receiver_type', 'subject', 'send_date']
    list_filter = ['created_at', 'receiver_type', 'send_date']
    search_fields = ['receiver_type', 'subject']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


@admin.register(SMSLog)
class SMSLogAdmin(admin.ModelAdmin):
    list_display = ['receiver_type', 'gateway', 'send_date']
    list_filter = ['created_at', 'receiver_type', 'send_date']
    search_fields = ['message', 'gateway']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


