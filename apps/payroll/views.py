"""
Views for payroll
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import SalaryGrade, SalaryPayment
from .serializers import (
    SalaryGradeListSerializer, SalaryGradeCreateSerializer, SalaryGradeDetailSerializer,
    SalaryPaymentListSerializer, SalaryPaymentCreateSerializer, SalaryPaymentDetailSerializer,
)


class SalaryGradeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for SalaryGrade
    Provides CRUD operations for SalaryGrade
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = '__all__'
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter by college for multi-tenancy"""
        queryset = SalaryGrade.objects.filter(is_deleted=False)

        # Filter by college if user is not superadmin
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)

        return queryset

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return SalaryGradeListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return SalaryGradeCreateSerializer
        return SalaryGradeDetailSerializer

    def perform_destroy(self, instance):
        """Soft delete"""
        instance.is_deleted = True
        instance.save()


class SalaryPaymentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for SalaryPayment
    Provides CRUD operations for SalaryPayment
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = '__all__'
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter by college for multi-tenancy"""
        queryset = SalaryPayment.objects.filter(is_deleted=False)

        # Filter by college if user is not superadmin
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)

        return queryset

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return SalaryPaymentListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return SalaryPaymentCreateSerializer
        return SalaryPaymentDetailSerializer

    def perform_destroy(self, instance):
        """Soft delete"""
        instance.is_deleted = True
        instance.save()

