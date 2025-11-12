"""
Django admin configuration for payroll
"""
from django.contrib import admin
from .models import SalaryGrade, SalaryPayment


@admin.register(SalaryGrade)
class SalaryGradeAdmin(admin.ModelAdmin):
    list_display = ['grade_name', 'basic_salary', 'gross_salary', 'net_salary']
    list_filter = ['created_at']
    search_fields = ['grade_name', 'basic_salary', 'gross_salary']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


@admin.register(SalaryPayment)
class SalaryPaymentAdmin(admin.ModelAdmin):
    list_display = ['employee_type', 'salary_month', 'gross_salary', 'net_salary']
    list_filter = ['created_at']
    search_fields = ['employee_type', 'salary_month', 'gross_salary']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


