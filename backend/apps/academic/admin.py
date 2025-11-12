"""Academic admin"""
from django.contrib import admin
from .models import SchoolClass, ClassSection, Subject, Syllabus, StudyMaterial

@admin.register(SchoolClass)
class SchoolClassAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'numeric_name', 'class_teacher']
    search_fields = ['name']

@admin.register(ClassSection)
class ClassSectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'school_class', 'section_teacher']
    search_fields = ['name']
    list_filter = ['school_class']

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'subject_code', 'subject_type', 'school_class']
    search_fields = ['name', 'subject_code']
    list_filter = ['subject_type', 'school_class']

@admin.register(Syllabus)
class SyllabusAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'school_class', 'subject', 'session_year']
    search_fields = ['title']
    list_filter = ['school_class', 'subject']

@admin.register(StudyMaterial)
class StudyMaterialAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'school_class', 'subject']
    search_fields = ['title']
    list_filter = ['school_class', 'subject']
