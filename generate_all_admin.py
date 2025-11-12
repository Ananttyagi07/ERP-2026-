#!/usr/bin/env python3
"""
Generate Django admin for all 16 Superadmin Phase 3 modules
"""

import os

# Model definitions for each module with key fields
MODULE_MODELS = {
    'asset_management': {
        'Vendor': ['name', 'email', 'phone', 'contact_name'],
        'Store': ['name', 'store_code', 'description'],
        'AssetCategory': ['name', 'description'],
        'AssetItem': ['name', 'product_code', 'item_type', 'category', 'store'],
        'AssetPurchase': ['item', 'quantity', 'unit_price', 'vendor', 'purchase_date'],
        'AssetIssue': ['item', 'quantity', 'issued_to_type', 'issue_date']
    },
    'library': {
        'Book': ['title', 'book_id', 'isbn_no', 'author', 'quantity'],
        'LibraryMember': ['student', 'library_id', 'is_active'],
        'BookIssue': ['book', 'member', 'issue_date', 'due_date', 'return_date'],
        'EBook': ['title', 'author', 'isbn_no', 'subject']
    },
    'transport': {
        'Vehicle': ['vehicle_number', 'vehicle_model', 'driver_name', 'driver_contact'],
        'TransportRoute': ['route_name', 'route_start', 'route_end'],
        'RouteStop': ['route', 'vehicle', 'stop_name', 'stop_fare'],
        'TransportMember': ['student', 'route', 'stop', 'vehicle']
    },
    'messaging': {
        'Message': ['sender', 'receiver', 'subject', 'is_read', 'is_draft']
    },
    'communication': {
        'EmailLog': ['receiver_type', 'subject', 'sent_at'],
        'SMSLog': ['message', 'gateway', 'sent_at']
    },
    'complain': {
        'ComplainType': ['name', 'description'],
        'Complain': ['complain_type', 'complain_by_type', 'subject', 'date']
    },
    'announcement': {
        'Notice': ['title', 'date', 'is_view_on_web'],
        'News': ['title', 'date', 'is_view_on_web'],
        'Holiday': ['title', 'from_date', 'to_date', 'is_view_on_web']
    },
    'scholarship': {
        'ScholarshipCandidate': ['student', 'amount', 'remarks'],
        'Donor': ['name', 'phone', 'email'],
        'Scholarship': ['candidate', 'donor', 'amount', 'payment_date']
    },
    'event': {
        'Event': ['title', 'event_from', 'event_to', 'is_view_on_web']
    },
    'payroll': {
        'SalaryGrade': ['grade_name', 'basic_salary', 'gross_salary', 'net_salary'],
        'SalaryPayment': ['employee_type', 'salary_month', 'gross_salary', 'net_salary']
    },
    'accounting': {
        'Discount': ['name', 'discount_type', 'amount', 'percentage'],
        'FeeType': ['name', 'description'],
        'Invoice': ['invoice_number', 'student', 'gross_amount', 'net_amount', 'paid_status'],
        'Payment': ['invoice', 'amount', 'payment_method', 'payment_date'],
        'IncomeHead': ['name', 'description'],
        'Income': ['income_head', 'amount', 'date'],
        'ExpenditureHead': ['name', 'description'],
        'Expenditure': ['expenditure_head', 'amount', 'date']
    },
    'media_gallery': {
        'Gallery': ['title', 'description', 'is_view_on_web'],
        'GalleryImage': ['gallery', 'title', 'image']
    },
    'frontend_cms': {
        'FrontendPage': ['page_title', 'page_slug', 'is_active'],
        'Slider': ['title', 'is_active'],
        'AboutSchool': ['title', 'description']
    },
    'miscellaneous': {
        'Award': ['award_to_type', 'award_name', 'gift', 'date'],
        'Todo': ['title', 'date', 'status', 'is_completed'],
        'FAQ': ['question', 'answer', 'is_active']
    },
    'subscription': {
        'SubscriptionPlan': ['name', 'plan_type', 'price', 'max_students'],
        'Subscription': ['college', 'plan', 'status', 'start_date', 'end_date'],
        'SubscriptionPayment': ['subscription', 'amount', 'payment_method', 'payment_date']
    }
}

def generate_admin(module_name, models_dict):
    """Generate admin.py for a module"""

    if not models_dict:
        content = f"""\"\"\"
Django admin configuration for {module_name}
\"\"\"
from django.contrib import admin
"""
        return content

    models = list(models_dict.keys())

    content = f"""\"\"\"
Django admin configuration for {module_name}
\"\"\"
from django.contrib import admin
from .models import {', '.join(models)}


"""

    # Generate admin classes
    for model, fields in models_dict.items():
        content += f"""@admin.register({model})
class {model}Admin(admin.ModelAdmin):
    list_display = [{', '.join([f"'{field}'" for field in fields[:5]])}]
    list_filter = ['created_at']
    search_fields = [{', '.join([f"'{field}'" for field in fields[:3]])}]
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


"""

    return content

def main():
    print("=" * 60)
    print("GENERATING ADMIN FOR ALL MODULES")
    print("=" * 60)
    print()

    for module, models_dict in MODULE_MODELS.items():
        print(f"Generating admin for {module}...")
        content = generate_admin(module, models_dict)

        file_path = f'apps/{module}/admin.py'
        with open(file_path, 'w') as f:
            f.write(content)

        print(f"  ✓ {file_path} ({len(models_dict)} models)")

    print()
    print("=" * 60)
    print("✓ All admin files generated successfully!")
    print("=" * 60)

if __name__ == '__main__':
    main()
