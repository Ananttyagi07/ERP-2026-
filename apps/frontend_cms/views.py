"""
Views for frontend_cms
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import FrontendPage, Slider, AboutSchool
from .serializers import (
    FrontendPageListSerializer, FrontendPageCreateSerializer, FrontendPageDetailSerializer,
    SliderListSerializer, SliderCreateSerializer, SliderDetailSerializer,
    AboutSchoolListSerializer, AboutSchoolCreateSerializer, AboutSchoolDetailSerializer,
)


class FrontendPageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for FrontendPage
    Provides CRUD operations for FrontendPage
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = '__all__'
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter by college for multi-tenancy"""
        queryset = FrontendPage.objects.filter(is_deleted=False)

        # Filter by college if user is not superadmin
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)

        return queryset

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return FrontendPageListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return FrontendPageCreateSerializer
        return FrontendPageDetailSerializer

    def perform_destroy(self, instance):
        """Soft delete"""
        instance.is_deleted = True
        instance.save()


class SliderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Slider
    Provides CRUD operations for Slider
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = '__all__'
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter by college for multi-tenancy"""
        queryset = Slider.objects.filter(is_deleted=False)

        # Filter by college if user is not superadmin
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)

        return queryset

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return SliderListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return SliderCreateSerializer
        return SliderDetailSerializer

    def perform_destroy(self, instance):
        """Soft delete"""
        instance.is_deleted = True
        instance.save()


class AboutSchoolViewSet(viewsets.ModelViewSet):
    """
    ViewSet for AboutSchool
    Provides CRUD operations for AboutSchool
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = '__all__'
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter by college for multi-tenancy"""
        queryset = AboutSchool.objects.filter(is_deleted=False)

        # Filter by college if user is not superadmin
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)

        return queryset

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return AboutSchoolListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return AboutSchoolCreateSerializer
        return AboutSchoolDetailSerializer

    def perform_destroy(self, instance):
        """Soft delete"""
        instance.is_deleted = True
        instance.save()

