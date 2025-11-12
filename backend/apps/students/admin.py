"""Students admin"""
from django.contrib import admin
from .models import Student, StudentParent

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'roll_number', 'school_class', 'section', 'admission_date']
    search_fields = ['user__email', 'roll_number', 'registration_number']
    list_filter = ['school_class', 'section', 'admission_date']

@admin.register(StudentParent)
class StudentParentAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'guardian', 'relationship', 'is_primary']
    list_filter = ['relationship', 'is_primary']
