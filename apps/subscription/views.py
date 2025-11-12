"""
Views for subscription
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import SubscriptionPlan, Subscription, SubscriptionPayment
from .serializers import (
    SubscriptionPlanListSerializer, SubscriptionPlanCreateSerializer, SubscriptionPlanDetailSerializer,
    SubscriptionListSerializer, SubscriptionCreateSerializer, SubscriptionDetailSerializer,
    SubscriptionPaymentListSerializer, SubscriptionPaymentCreateSerializer, SubscriptionPaymentDetailSerializer,
)


class SubscriptionPlanViewSet(viewsets.ModelViewSet):
    """
    ViewSet for SubscriptionPlan
    Provides CRUD operations for SubscriptionPlan
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = '__all__'
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter by college for multi-tenancy"""
        queryset = SubscriptionPlan.objects.filter(is_deleted=False)

        # Filter by college if user is not superadmin
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)

        return queryset

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return SubscriptionPlanListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return SubscriptionPlanCreateSerializer
        return SubscriptionPlanDetailSerializer

    def perform_destroy(self, instance):
        """Soft delete"""
        instance.is_deleted = True
        instance.save()


class SubscriptionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Subscription
    Provides CRUD operations for Subscription
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = '__all__'
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter by college for multi-tenancy"""
        queryset = Subscription.objects.filter(is_deleted=False)

        # Filter by college if user is not superadmin
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)

        return queryset

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return SubscriptionListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return SubscriptionCreateSerializer
        return SubscriptionDetailSerializer

    def perform_destroy(self, instance):
        """Soft delete"""
        instance.is_deleted = True
        instance.save()


class SubscriptionPaymentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for SubscriptionPayment
    Provides CRUD operations for SubscriptionPayment
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = '__all__'
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter by college for multi-tenancy"""
        queryset = SubscriptionPayment.objects.filter(is_deleted=False)

        # Filter by college if user is not superadmin
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)

        return queryset

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return SubscriptionPaymentListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return SubscriptionPaymentCreateSerializer
        return SubscriptionPaymentDetailSerializer

    def perform_destroy(self, instance):
        """Soft delete"""
        instance.is_deleted = True
        instance.save()

