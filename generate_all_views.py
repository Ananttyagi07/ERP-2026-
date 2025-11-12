#!/usr/bin/env python3
"""
Generate views (ViewSets) for all 16 Superadmin Phase 3 modules
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
    'reporting': [],  # No models, just custom views
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

def generate_views(module_name, models):
    """Generate views.py for a module"""

    if not models:
        # For reporting module, create placeholder
        if module_name == 'reporting':
            content = """\"\"\"
Views for reporting module
Custom report generation views
\"\"\"
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


class StudentReportView(APIView):
    \"\"\"Generate student reports\"\"\"
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # TODO: Implement student report generation
        return Response({'message': 'Student report endpoint'}, status=status.HTTP_200_OK)


class AttendanceReportView(APIView):
    \"\"\"Generate attendance reports\"\"\"
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # TODO: Implement attendance report generation
        return Response({'message': 'Attendance report endpoint'}, status=status.HTTP_200_OK)


class FinanceReportView(APIView):
    \"\"\"Generate finance reports\"\"\"
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # TODO: Implement finance report generation
        return Response({'message': 'Finance report endpoint'}, status=status.HTTP_200_OK)
"""
            return content
        else:
            content = f"""\"\"\"
Views for {module_name}
\"\"\"
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
"""
            return content

    content = f"""\"\"\"
Views for {module_name}
\"\"\"
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import {', '.join(models)}
from .serializers import (
"""

    # Add serializer imports
    for model in models:
        content += f"    {model}ListSerializer, {model}CreateSerializer, {model}DetailSerializer,\n"

    content += ")\n\n"

    # Generate ViewSets
    for model in models:
        content += f"""
class {model}ViewSet(viewsets.ModelViewSet):
    \"\"\"
    ViewSet for {model}
    Provides CRUD operations for {model}
    \"\"\"
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = '__all__'
    ordering = ['-created_at']

    def get_queryset(self):
        \"\"\"Filter by college for multi-tenancy\"\"\"
        queryset = {model}.objects.filter(is_deleted=False)

        # Filter by college if user is not superadmin
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)

        return queryset

    def get_serializer_class(self):
        \"\"\"Return appropriate serializer based on action\"\"\"
        if self.action == 'list':
            return {model}ListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return {model}CreateSerializer
        return {model}DetailSerializer

    def perform_destroy(self, instance):
        \"\"\"Soft delete\"\"\"
        instance.is_deleted = True
        instance.save()

"""

    return content

def main():
    print("=" * 60)
    print("GENERATING VIEWS FOR ALL MODULES")
    print("=" * 60)
    print()

    for module, models in MODULE_MODELS.items():
        print(f"Generating views for {module}...")
        content = generate_views(module, models)

        file_path = f'apps/{module}/views.py'
        with open(file_path, 'w') as f:
            f.write(content)

        print(f"  ✓ {file_path} ({len(models)} ViewSets)")

    print()
    print("=" * 60)
    print("✓ All views generated successfully!")
    print("=" * 60)

if __name__ == '__main__':
    main()
