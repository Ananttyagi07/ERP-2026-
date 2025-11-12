#!/usr/bin/env python3
"""
Generate apps.py configuration files for all 9 new modules
"""

APPS_CONFIG = {
    'apps/student_management/apps.py': '''from django.apps import AppConfig


class StudentManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.student_management'
    verbose_name = 'Student Management'
''',

    'apps/attendance/apps.py': '''from django.apps import AppConfig


class AttendanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.attendance'
    verbose_name = 'Attendance'
''',

    'apps/card_generation/apps.py': '''from django.apps import AppConfig


class CardGenerationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.card_generation'
    verbose_name = 'Card Generation'
''',

    'apps/online_exam/apps.py': '''from django.apps import AppConfig


class OnlineExamConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.online_exam'
    verbose_name = 'Online Exam'
''',

    'apps/exam_management/apps.py': '''from django.apps import AppConfig


class ExamManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.exam_management'
    verbose_name = 'Exam Management'
''',

    'apps/marks/apps.py': '''from django.apps import AppConfig


class MarksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.marks'
    verbose_name = 'Marks Management'
''',

    'apps/promotion/apps.py': '''from django.apps import AppConfig


class PromotionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.promotion'
    verbose_name = 'Student Promotion'
''',

    'apps/certificates/apps.py': '''from django.apps import AppConfig


class CertificatesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.certificates'
    verbose_name = 'Certificates'
''',

    'apps/inventory/apps.py': '''from django.apps import AppConfig


class InventoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.inventory'
    verbose_name = 'Inventory Management'
''',
}

print("🚀 Generating apps.py configuration files...")
print("=" * 70)

for filepath, content in APPS_CONFIG.items():
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"✓ {filepath}")

print("\n✅ All apps.py files created successfully!")
