"""
Django admin configuration for scholarship
"""
from django.contrib import admin
from .models import ScholarshipCandidate, Donor, Scholarship


@admin.register(ScholarshipCandidate)
class ScholarshipCandidateAdmin(admin.ModelAdmin):
    list_display = ['student', 'amount', 'remarks']
    list_filter = ['created_at']
    search_fields = ['student', 'amount', 'remarks']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email']
    list_filter = ['created_at']
    search_fields = ['name', 'phone', 'email']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


@admin.register(Scholarship)
class ScholarshipAdmin(admin.ModelAdmin):
    list_display = ['candidate', 'donor', 'amount', 'payment_date']
    list_filter = ['created_at']
    search_fields = ['candidate', 'donor', 'amount']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


