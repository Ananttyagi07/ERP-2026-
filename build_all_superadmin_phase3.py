#!/usr/bin/env python3
"""
Complete build script for all 16 remaining Superadmin modules
Creates directories, apps.py, serializers, views, URLs, and admin
"""

import os
import sys

# Add project to path
sys.path.insert(0, '/home/anant/ERP-MAIN-PROJECT')

MODULES = [
    'asset_management',
    'library',
    'transport',
    'messaging',
    'communication',
    'complain',
    'announcement',
    'scholarship',
    'event',
    'payroll',
    'accounting',
    'reporting',
    'media_gallery',
    'frontend_cms',
    'miscellaneous',
    'subscription'
]

def create_directories():
    """Create all module directories"""
    print("Creating module directories...")
    for module in MODULES:
        module_path = f'apps/{module}'
        os.makedirs(module_path, exist_ok=True)

        # Create __init__.py
        init_file = f'{module_path}/__init__.py'
        if not os.path.exists(init_file):
            with open(init_file, 'w') as f:
                f.write('')
        print(f"  ✓ {module}")
    print()

def create_apps_config():
    """Generate apps.py for all modules"""
    print("Generating apps.py files...")

    module_configs = {
        'asset_management': 'AssetManagement',
        'library': 'Library',
        'transport': 'Transport',
        'messaging': 'Messaging',
        'communication': 'Communication',
        'complain': 'Complain',
        'announcement': 'Announcement',
        'scholarship': 'Scholarship',
        'event': 'Event',
        'payroll': 'Payroll',
        'accounting': 'Accounting',
        'reporting': 'Reporting',
        'media_gallery': 'MediaGallery',
        'frontend_cms': 'FrontendCms',
        'miscellaneous': 'Miscellaneous',
        'subscription': 'Subscription'
    }

    for module, class_name in module_configs.items():
        apps_content = f"""from django.apps import AppConfig


class {class_name}Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.{module}'
    verbose_name = '{class_name}'
"""
        with open(f'apps/{module}/apps.py', 'w') as f:
            f.write(apps_content)
        print(f"  ✓ {module}/apps.py")
    print()

if __name__ == '__main__':
    print("=" * 60)
    print("SUPERADMIN PHASE 3 - DIRECTORY & CONFIG SETUP")
    print("=" * 60)
    print()

    create_directories()
    create_apps_config()

    print("=" * 60)
    print("✓ Directory and config setup complete!")
    print("=" * 60)
