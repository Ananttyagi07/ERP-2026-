"""HR admin"""
from django.contrib import admin
from .models import Designation, Employee

@admin.register(Designation)
class DesignationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at']
    search_fields = ['name']

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'designation', 'joining_date']
    search_fields = ['user__email', 'user__username']
    list_filter = ['designation', 'joining_date']
