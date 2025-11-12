"""
Views for communication
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import EmailLog, SMSLog
from .serializers import (
    EmailLogListSerializer, EmailLogCreateSerializer, EmailLogDetailSerializer,
    SMSLogListSerializer, SMSLogCreateSerializer, SMSLogDetailSerializer,
)


class EmailLogViewSet(viewsets.ModelViewSet):
    """
    ViewSet for EmailLog
    Provides CRUD operations for EmailLog
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = '__all__'
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter by college for multi-tenancy"""
        queryset = EmailLog.objects.filter(is_deleted=False)

        # Filter by college if user is not superadmin
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)

        return queryset

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return EmailLogListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return EmailLogCreateSerializer
        return EmailLogDetailSerializer

    def perform_destroy(self, instance):
        """Soft delete"""
        instance.is_deleted = True
        instance.save()


class SMSLogViewSet(viewsets.ModelViewSet):
    """
    ViewSet for SMSLog
    Provides CRUD operations for SMSLog
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = '__all__'
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter by college for multi-tenancy"""
        queryset = SMSLog.objects.filter(is_deleted=False)

        # Filter by college if user is not superadmin
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)

        return queryset

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return SMSLogListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return SMSLogCreateSerializer
        return SMSLogDetailSerializer

    def perform_destroy(self, instance):
        """Soft delete"""
        instance.is_deleted = True
        instance.save()

