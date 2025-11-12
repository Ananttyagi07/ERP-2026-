#!/usr/bin/env python3
"""
Generate serializers for all 16 Superadmin Phase 3 modules
"""

import os

# Model definitions for each module
MODULE_MODELS = {
    'asset_management': [
        'Vendor', 'Store', 'AssetCategory', 'AssetItem', 'AssetPurchase', 'AssetIssue'
    ],
    'library': [
        'Book', 'LibraryMember', 'BookIssue', 'EBook'
    ],
    'transport': [
        'Vehicle', 'TransportRoute', 'RouteStop', 'TransportMember'
    ],
    'messaging': [
        'Message'
    ],
    'communication': [
        'EmailLog', 'SMSLog'
    ],
    'complain': [
        'ComplainType', 'Complain'
    ],
    'announcement': [
        'Notice', 'News', 'Holiday'
    ],
    'scholarship': [
        'ScholarshipCandidate', 'Donor', 'Scholarship'
    ],
    'event': [
        'Event'
    ],
    'payroll': [
        'SalaryGrade', 'SalaryPayment'
    ],
    'accounting': [
        'Discount', 'FeeType', 'Invoice', 'Payment', 'IncomeHead', 'Income', 'ExpenditureHead', 'Expenditure'
    ],
    'reporting': [],  # No models, just views
    'media_gallery': [
        'Gallery', 'GalleryImage'
    ],
    'frontend_cms': [
        'FrontendPage', 'Slider', 'AboutSchool'
    ],
    'miscellaneous': [
        'Award', 'Todo', 'FAQ'
    ],
    'subscription': [
        'SubscriptionPlan', 'Subscription', 'SubscriptionPayment'
    ]
}

def generate_serializers(module_name, models):
    """Generate serializers.py for a module"""

    if not models:
        # Empty serializers file for modules with no models
        content = """\"\"\"
Serializers for {module_name}
\"\"\"
from rest_framework import serializers
""".format(module_name=module_name)
        return content

    content = f"""\"\"\"
Serializers for {module_name}
\"\"\"
from rest_framework import serializers
from .models import {', '.join(models)}


"""

    for model in models:
        # List serializer (basic fields)
        content += f"""class {model}ListSerializer(serializers.ModelSerializer):
    \"\"\"List serializer for {model}\"\"\"

    class Meta:
        model = {model}
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


"""

        # Create/Update serializer
        content += f"""class {model}CreateSerializer(serializers.ModelSerializer):
    \"\"\"Create/Update serializer for {model}\"\"\"

    class Meta:
        model = {model}
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


"""

        # Detail serializer (all fields with relations)
        content += f"""class {model}DetailSerializer(serializers.ModelSerializer):
    \"\"\"Detail serializer for {model}\"\"\"

    class Meta:
        model = {model}
        fields = '__all__'
        depth = 1


"""

    return content

def main():
    print("=" * 60)
    print("GENERATING SERIALIZERS FOR ALL MODULES")
    print("=" * 60)
    print()

    for module, models in MODULE_MODELS.items():
        print(f"Generating serializers for {module}...")
        content = generate_serializers(module, models)

        file_path = f'apps/{module}/serializers.py'
        with open(file_path, 'w') as f:
            f.write(content)

        print(f"  ✓ {file_path} ({len(models)} models)")

    print()
    print("=" * 60)
    print("✓ All serializers generated successfully!")
    print("=" * 60)

if __name__ == '__main__':
    main()
