#!/usr/bin/env python3
"""
Script to generate correct admin.py files by reading models
"""
import os
import ast
import re

# Phase 3 apps to fix
APPS_TO_FIX = [
    'complain',
    'announcement',
    'scholarship',
    'event',
    'payroll',
    'media_gallery',
    'frontend_cms',
    'miscellaneous',
    'subscription',
]

def get_model_fields(model_file):
    """Extract all fields from a Django model file"""
    if not os.path.exists(model_file):
        return {}

    with open(model_file, 'r') as f:
        content = f.read()

    # Parse the file
    try:
        tree = ast.parse(content)
    except:
        return {}

    models = {}

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            # Get model name
            model_name = node.name
            if model_name.startswith('_'):
                continue

            fields = []
            for item in node.body:
                if isinstance(item, ast.Assign):
                    for target in item.targets:
                        if isinstance(target, ast.Name):
                            field_name = target.id
                            # Skip Meta and private fields
                            if field_name != 'Meta' and not field_name.startswith('_'):
                                fields.append(field_name)

            if fields:
                models[model_name] = fields

    return models

def print_models_and_fields():
    """Print all models and their fields for manual verification"""
    base_path = '/home/anant/ERP-MAIN-PROJECT/backend/apps'

    for app in APPS_TO_FIX:
        model_file = os.path.join(base_path, app, 'models.py')
        admin_file = os.path.join(base_path, app, 'admin.py')

        if not os.path.exists(model_file):
            print(f"\n{app}: NO MODELS FILE")
            continue

        if not os.path.exists(admin_file):
            print(f"\n{app}: NO ADMIN FILE")
            continue

        models = get_model_fields(model_file)

        print(f"\n{'='*60}")
        print(f"APP: {app}")
        print(f"{'='*60}")

        for model_name, fields in models.items():
            print(f"\n{model_name}:")
            print(f"  Fields: {', '.join(fields[:10])}")
            if len(fields) > 10:
                print(f"  ... and {len(fields) - 10} more")

if __name__ == '__main__':
    print_models_and_fields()
