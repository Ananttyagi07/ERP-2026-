"""Guardians admin"""
from django.contrib import admin
from .models import Guardian

@admin.register(Guardian)
class GuardianAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'occupation', 'phone_display']
    search_fields = ['user__email', 'user__username']

    def phone_display(self, obj):
        return obj.user.phone if obj.user else ''
    phone_display.short_description = 'Phone'
