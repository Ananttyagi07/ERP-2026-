#!/usr/bin/env python3
"""Generate Django admin registrations for all models"""

ADMIN_FILES = {
    'apps/superadmin/admin.py': '''"""Superadmin admin"""
from django.contrib import admin
from .models import SuperAdminProfile

@admin.register(SuperAdminProfile)
class SuperAdminProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'national_id', 'birth_date', 'created_at']
    search_fields = ['user__email', 'user__username', 'national_id']
    list_filter = ['blood_group', 'religion', 'created_at']
''',

    'apps/templates/admin.py': '''"""Templates admin"""
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
''',

    'apps/front_office/admin.py': '''"""Front Office admin"""
from django.contrib import admin
from .models import VisitorPurpose, VisitorInfo, CallLog, PostalDispatch, PostalReceive

@admin.register(VisitorPurpose)
class VisitorPurposeAdmin(admin.ModelAdmin):
    list_display = ['id', 'purpose', 'created_at']
    search_fields = ['purpose']

@admin.register(VisitorInfo)
class VisitorInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone', 'purpose', 'check_in_date', 'check_out_date']
    search_fields = ['name', 'phone', 'visitor_id']
    list_filter = ['check_in_date', 'meet_user_type']

@admin.register(CallLog)
class CallLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone', 'call_type', 'call_date']
    search_fields = ['name', 'phone']
    list_filter = ['call_type', 'call_date']

@admin.register(PostalDispatch)
class PostalDispatchAdmin(admin.ModelAdmin):
    list_display = ['id', 'to_title', 'reference_number', 'dispatch_date']
    search_fields = ['to_title', 'reference_number']
    list_filter = ['dispatch_date']

@admin.register(PostalReceive)
class PostalReceiveAdmin(admin.ModelAdmin):
    list_display = ['id', 'from_title', 'reference_number', 'receive_date', 'receiver_type']
    search_fields = ['from_title', 'reference_number']
    list_filter = ['receiver_type', 'receive_date']
''',

    'apps/hr/admin.py': '''"""HR admin"""
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
''',

    'apps/teachers/admin.py': '''"""Teachers admin"""
from django.contrib import admin
from .models import Department, Teacher, TeacherLecture, Rating

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'code', 'head']
    search_fields = ['name', 'code']

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'department', 'designation', 'joining_date']
    search_fields = ['user__email', 'user__username']
    list_filter = ['department', 'joining_date']

@admin.register(TeacherLecture)
class TeacherLectureAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'teacher', 'lecture_date', 'lecture_type']
    search_fields = ['title']
    list_filter = ['lecture_type', 'lecture_date']

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['id', 'rating_type', 'rating_value', 'created_at']
    list_filter = ['rating_type', 'created_at']
''',

    'apps/leave_management/admin.py': '''"""Leave Management admin"""
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
''',

    'apps/academic/admin.py': '''"""Academic admin"""
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
''',

    'apps/live_classes/admin.py': '''"""Live Classes admin"""
from django.contrib import admin
from .models import LiveClassType, LiveClass, Assignment

@admin.register(LiveClassType)
class LiveClassTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at']
    search_fields = ['name']

@admin.register(LiveClass)
class LiveClassAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'teacher', 'class_date', 'start_time', 'status']
    search_fields = ['subject__name']
    list_filter = ['status', 'class_date']

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'school_class', 'section', 'subject', 'submission_date', 'status']
    search_fields = ['title']
    list_filter = ['status', 'assignment_date']
''',

    'apps/students/admin.py': '''"""Students admin"""
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
''',

    'apps/guardians/admin.py': '''"""Guardians admin"""
from django.contrib import admin
from .models import Guardian

@admin.register(Guardian)
class GuardianAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'occupation', 'phone_display']
    search_fields = ['user__email', 'user__username']

    def phone_display(self, obj):
        return obj.user.phone if obj.user else ''
    phone_display.short_description = 'Phone'
''',
}

print("🚀 Generating Django admin registrations...")
print("=" * 60)

for filepath, content in ADMIN_FILES.items():
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"✓ {filepath}")

print("\n✅ All admin registrations created!")
print("=" * 60)
