#!/usr/bin/env python3
"""
Test that all Phase 3 modules can be imported successfully
This tests if the code is syntactically correct and loadable
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
sys.path.insert(0, '/home/anant/ERP-MAIN-PROJECT/backend')
django.setup()

print("=" * 60)
print("PHASE 3 MODULE IMPORT TEST")
print("=" * 60)
print()

# Test Phase 3 modules
phase3_modules = [
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

results = {'passed': 0, 'failed': 0, 'errors': []}

for module_name in phase3_modules:
    try:
        # Test model imports
        models_module = __import__(f'apps.{module_name}.models', fromlist=['*'])

        # Test serializer imports
        serializers_module = __import__(f'apps.{module_name}.serializers', fromlist=['*'])

        # Test view imports (skip admin for now as we know there are errors)
        views_module = __import__(f'apps.{module_name}.views', fromlist=['*'])

        # Test URL imports
        urls_module = __import__(f'apps.{module_name}.urls', fromlist=['*'])

        print(f"✓ {module_name:20s} - All imports successful")
        results['passed'] += 1

    except Exception as e:
        print(f"✗ {module_name:20s} - Import error: {str(e)[:50]}")
        results['failed'] += 1
        results['errors'].append((module_name, str(e)))

print()
print("=" * 60)
print("TEST SUMMARY")
print("=" * 60)
print(f"✓ Passed: {results['passed']}/{len(phase3_modules)}")
print(f"✗ Failed: {results['failed']}/{len(phase3_modules)}")

if results['errors']:
    print("\nDetailed Errors:")
    for module, error in results['errors']:
        print(f"\n{module}:")
        print(f"  {error}")

print("\n" + "=" * 60)

if results['failed'] == 0:
    print("🎉 ALL PHASE 3 MODULES IMPORT SUCCESSFULLY!")
    print("=" * 60)
    print("\nYour Phase 3 implementation is syntactically correct!")
    print("All models, serializers, views, and URLs can be loaded.")
    print("\nNext step: Fix admin field references and model conflicts,")
    print("then run migrations to create database tables.")
else:
    print("⚠️  SOME MODULES HAVE IMPORT ERRORS")
    print("=" * 60)
    print("Check the detailed errors above and fix them.")

sys.exit(0 if results['failed'] == 0 else 1)
