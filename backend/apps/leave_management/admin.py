"""Leave Management admin"""
from django.contrib import admin
from .models import LeaveType, LeaveApplication

@admin.register(LeaveType)
class LeaveTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'applicant_type', 'days_allowed']
    search_fields = ['name']
    list_filter = ['applicant_type']

@admin.register(LeaveApplication)
class LeaveApplicationAdmin(admin.ModelAdmin):
    list_display = ['id', 'applicant', 'leave_type', 'start_date', 'end_date', 'status']
    search_fields = ['applicant__email']
    list_filter = ['status', 'start_date']
