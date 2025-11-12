"""
Django admin configuration for scholarship
"""
from django.contrib import admin
from .models import ScholarshipCandidate, Donor, Scholarship


@admin.register(ScholarshipCandidate)
class ScholarshipCandidateAdmin(admin.ModelAdmin):
    list_display = ['student', 'school_class', 'section']
    list_filter = ['created_at', 'school_class']
    search_fields = ['student__user__email']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = ['donor_name', 'donor_type', 'phone', 'email']
    list_filter = ['created_at', 'donor_type']
    search_fields = ['donor_name', 'contact_name', 'email']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


@admin.register(Scholarship)
class ScholarshipAdmin(admin.ModelAdmin):
    list_display = ['candidate', 'amount', 'payment_date']
    list_filter = ['created_at', 'payment_date']
    search_fields = ['candidate__student__user__email']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


