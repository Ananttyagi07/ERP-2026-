#!/usr/bin/env python3
"""
Generate URLs for all 16 Superadmin Phase 3 modules
"""

import os

# Model definitions for each module
MODULE_MODELS = {
    'asset_management': [
        ('Vendor', 'vendors'),
        ('Store', 'stores'),
        ('AssetCategory', 'asset-categories'),
        ('AssetItem', 'asset-items'),
        ('AssetPurchase', 'asset-purchases'),
        ('AssetIssue', 'asset-issues')
    ],
    'library': [
        ('Book', 'books'),
        ('LibraryMember', 'library-members'),
        ('BookIssue', 'book-issues'),
        ('EBook', 'ebooks')
    ],
    'transport': [
        ('Vehicle', 'vehicles'),
        ('TransportRoute', 'routes'),
        ('RouteStop', 'route-stops'),
        ('TransportMember', 'transport-members')
    ],
    'messaging': [
        ('Message', 'messages')
    ],
    'communication': [
        ('EmailLog', 'email-logs'),
        ('SMSLog', 'sms-logs')
    ],
    'complain': [
        ('ComplainType', 'complain-types'),
        ('Complain', 'complains')
    ],
    'announcement': [
        ('Notice', 'notices'),
        ('News', 'news'),
        ('Holiday', 'holidays')
    ],
    'scholarship': [
        ('ScholarshipCandidate', 'scholarship-candidates'),
        ('Donor', 'donors'),
        ('Scholarship', 'scholarships')
    ],
    'event': [
        ('Event', 'events')
    ],
    'payroll': [
        ('SalaryGrade', 'salary-grades'),
        ('SalaryPayment', 'salary-payments')
    ],
    'accounting': [
        ('Discount', 'discounts'),
        ('FeeType', 'fee-types'),
        ('Invoice', 'invoices'),
        ('Payment', 'payments'),
        ('IncomeHead', 'income-heads'),
        ('Income', 'incomes'),
        ('ExpenditureHead', 'expenditure-heads'),
        ('Expenditure', 'expenditures')
    ],
    'reporting': [],  # Custom views, not ViewSets
    'media_gallery': [
        ('Gallery', 'galleries'),
        ('GalleryImage', 'gallery-images')
    ],
    'frontend_cms': [
        ('FrontendPage', 'frontend-pages'),
        ('Slider', 'sliders'),
        ('AboutSchool', 'about-school')
    ],
    'miscellaneous': [
        ('Award', 'awards'),
        ('Todo', 'todos'),
        ('FAQ', 'faqs')
    ],
    'subscription': [
        ('SubscriptionPlan', 'subscription-plans'),
        ('Subscription', 'subscriptions'),
        ('SubscriptionPayment', 'subscription-payments')
    ]
}

def generate_urls(module_name, models):
    """Generate urls.py for a module"""

    if module_name == 'reporting':
        # Special case for reporting module
        content = """\"\"\"
URL Configuration for reporting
\"\"\"
from django.urls import path
from .views import StudentReportView, AttendanceReportView, FinanceReportView

app_name = 'reporting'

urlpatterns = [
    path('student/', StudentReportView.as_view(), name='student-report'),
    path('attendance/', AttendanceReportView.as_view(), name='attendance-report'),
    path('finance/', FinanceReportView.as_view(), name='finance-report'),
]
"""
        return content

    if not models:
        content = f"""\"\"\"
URL Configuration for {module_name}
\"\"\"
from django.urls import path

app_name = '{module_name}'

urlpatterns = []
"""
        return content

    content = f"""\"\"\"
URL Configuration for {module_name}
\"\"\"
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import {', '.join([model[0] + 'ViewSet' for model in models])}

app_name = '{module_name}'

router = DefaultRouter()
"""

    # Register all ViewSets
    for model_name, url_name in models:
        content += f"router.register(r'{url_name}', {model_name}ViewSet, basename='{url_name}')\n"

    content += """
urlpatterns = [
    path('', include(router.urls)),
]
"""

    return content

def main():
    print("=" * 60)
    print("GENERATING URLS FOR ALL MODULES")
    print("=" * 60)
    print()

    for module, models in MODULE_MODELS.items():
        print(f"Generating URLs for {module}...")
        content = generate_urls(module, models)

        file_path = f'apps/{module}/urls.py'
        with open(file_path, 'w') as f:
            f.write(content)

        print(f"  ✓ {file_path} ({len(models)} routes)")

    print()
    print("=" * 60)
    print("✓ All URLs generated successfully!")
    print("=" * 60)

if __name__ == '__main__':
    main()
