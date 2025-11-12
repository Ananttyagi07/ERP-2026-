"""Templates admin"""
from django.contrib import admin
from .models import SMSTemplate, EmailTemplate

@admin.register(SMSTemplate)
class SMSTemplateAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'is_active', 'created_at']
    search_fields = ['name', 'message_body']
    list_filter = ['is_active', 'created_at']

@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'subject', 'is_active', 'created_at']
    search_fields = ['name', 'subject', 'message_body']
    list_filter = ['is_active', 'created_at']
