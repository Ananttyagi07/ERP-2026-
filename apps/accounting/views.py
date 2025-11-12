"""
Views for accounting
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Discount, FeeType, Invoice, Payment, IncomeHead, Income, ExpenditureHead, Expenditure
from .serializers import (
    DiscountListSerializer, DiscountCreateSerializer, DiscountDetailSerializer,
    FeeTypeListSerializer, FeeTypeCreateSerializer, FeeTypeDetailSerializer,
    InvoiceListSerializer, InvoiceCreateSerializer, InvoiceDetailSerializer,
    PaymentListSerializer, PaymentCreateSerializer, PaymentDetailSerializer,
    IncomeHeadListSerializer, IncomeHeadCreateSerializer, IncomeHeadDetailSerializer,
    IncomeListSerializer, IncomeCreateSerializer, IncomeDetailSerializer,
    ExpenditureHeadListSerializer, ExpenditureHeadCreateSerializer, ExpenditureHeadDetailSerializer,
    ExpenditureListSerializer, ExpenditureCreateSerializer, ExpenditureDetailSerializer,
)


class DiscountViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Discount
    Provides CRUD operations for Discount
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = '__all__'
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter by college for multi-tenancy"""
        queryset = Discount.objects.filter(is_deleted=False)

        # Filter by college if user is not superadmin
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)

        return queryset

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return DiscountListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return DiscountCreateSerializer
        return DiscountDetailSerializer

    def perform_destroy(self, instance):
        """Soft delete"""
        instance.is_deleted = True
        instance.save()


class FeeTypeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for FeeType
    Provides CRUD operations for FeeType
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = '__all__'
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter by college for multi-tenancy"""
        queryset = FeeType.objects.filter(is_deleted=False)

        # Filter by college if user is not superadmin
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)

        return queryset

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return FeeTypeListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return FeeTypeCreateSerializer
        return FeeTypeDetailSerializer

    def perform_destroy(self, instance):
        """Soft delete"""
        instance.is_deleted = True
        instance.save()


class InvoiceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Invoice
    Provides CRUD operations for Invoice
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = '__all__'
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter by college for multi-tenancy"""
        queryset = Invoice.objects.filter(is_deleted=False)

        # Filter by college if user is not superadmin
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)

        return queryset

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return InvoiceListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return InvoiceCreateSerializer
        return InvoiceDetailSerializer

    def perform_destroy(self, instance):
        """Soft delete"""
        instance.is_deleted = True
        instance.save()


class PaymentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Payment
    Provides CRUD operations for Payment
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = '__all__'
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter by college for multi-tenancy"""
        queryset = Payment.objects.filter(is_deleted=False)

        # Filter by college if user is not superadmin
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)

        return queryset

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return PaymentListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return PaymentCreateSerializer
        return PaymentDetailSerializer

    def perform_destroy(self, instance):
        """Soft delete"""
        instance.is_deleted = True
        instance.save()


class IncomeHeadViewSet(viewsets.ModelViewSet):
    """
    ViewSet for IncomeHead
    Provides CRUD operations for IncomeHead
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = '__all__'
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter by college for multi-tenancy"""
        queryset = IncomeHead.objects.filter(is_deleted=False)

        # Filter by college if user is not superadmin
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)

        return queryset

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return IncomeHeadListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return IncomeHeadCreateSerializer
        return IncomeHeadDetailSerializer

    def perform_destroy(self, instance):
        """Soft delete"""
        instance.is_deleted = True
        instance.save()


class IncomeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Income
    Provides CRUD operations for Income
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = '__all__'
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter by college for multi-tenancy"""
        queryset = Income.objects.filter(is_deleted=False)

        # Filter by college if user is not superadmin
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)

        return queryset

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return IncomeListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return IncomeCreateSerializer
        return IncomeDetailSerializer

    def perform_destroy(self, instance):
        """Soft delete"""
        instance.is_deleted = True
        instance.save()


class ExpenditureHeadViewSet(viewsets.ModelViewSet):
    """
    ViewSet for ExpenditureHead
    Provides CRUD operations for ExpenditureHead
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = '__all__'
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter by college for multi-tenancy"""
        queryset = ExpenditureHead.objects.filter(is_deleted=False)

        # Filter by college if user is not superadmin
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)

        return queryset

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return ExpenditureHeadListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ExpenditureHeadCreateSerializer
        return ExpenditureHeadDetailSerializer

    def perform_destroy(self, instance):
        """Soft delete"""
        instance.is_deleted = True
        instance.save()


class ExpenditureViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Expenditure
    Provides CRUD operations for Expenditure
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = '__all__'
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter by college for multi-tenancy"""
        queryset = Expenditure.objects.filter(is_deleted=False)

        # Filter by college if user is not superadmin
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)

        return queryset

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return ExpenditureListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ExpenditureCreateSerializer
        return ExpenditureDetailSerializer

    def perform_destroy(self, instance):
        """Soft delete"""
        instance.is_deleted = True
        instance.save()

