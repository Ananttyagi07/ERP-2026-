#!/usr/bin/env python3
"""Generate apps.py config files for all apps"""

APPS = {
    'superadmin': 'Superadmin',
    'templates': 'Templates',
    'front_office': 'FrontOffice',
    'hr': 'Hr',
    'teachers': 'Teachers',
    'leave_management': 'LeaveManagement',
    'academic': 'Academic',
    'live_classes': 'LiveClasses',
    'students': 'Students',
    'guardians': 'Guardians',
}

for app_name, class_name in APPS.items():
    content = f'''"""
{class_name} app configuration
"""
from django.apps import AppConfig


class {class_name}Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.{app_name}'
    verbose_name = '{class_name}'
'''
    
    with open(f'apps/{app_name}/apps.py', 'w') as f:
        f.write(content)
    
    print(f"✓ Created apps/{app_name}/apps.py")

print(f"\n✅ Generated {len(APPS)} apps.py files!")
