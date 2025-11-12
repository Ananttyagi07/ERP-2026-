"""
Views for complain
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import ComplainType, Complain
from .serializers import (
    ComplainTypeListSerializer, ComplainTypeCreateSerializer, ComplainTypeDetailSerializer,
    ComplainListSerializer, ComplainCreateSerializer, ComplainDetailSerializer,
)


class ComplainTypeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for ComplainType
    Provides CRUD operations for ComplainType
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = '__all__'
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter by college for multi-tenancy"""
        queryset = ComplainType.objects.filter(is_deleted=False)

        # Filter by college if user is not superadmin
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)

        return queryset

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return ComplainTypeListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ComplainTypeCreateSerializer
        return ComplainTypeDetailSerializer

    def perform_destroy(self, instance):
        """Soft delete"""
        instance.is_deleted = True
        instance.save()


class ComplainViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Complain
    Provides CRUD operations for Complain
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = '__all__'
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter by college for multi-tenancy"""
        queryset = Complain.objects.filter(is_deleted=False)

        # Filter by college if user is not superadmin
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)

        return queryset

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return ComplainListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ComplainCreateSerializer
        return ComplainDetailSerializer

    def perform_destroy(self, instance):
        """Soft delete"""
        instance.is_deleted = True
        instance.save()

