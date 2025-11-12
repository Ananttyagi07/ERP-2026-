"""
Views for scholarship
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import ScholarshipCandidate, Donor, Scholarship
from .serializers import (
    ScholarshipCandidateListSerializer, ScholarshipCandidateCreateSerializer, ScholarshipCandidateDetailSerializer,
    DonorListSerializer, DonorCreateSerializer, DonorDetailSerializer,
    ScholarshipListSerializer, ScholarshipCreateSerializer, ScholarshipDetailSerializer,
)


class ScholarshipCandidateViewSet(viewsets.ModelViewSet):
    """
    ViewSet for ScholarshipCandidate
    Provides CRUD operations for ScholarshipCandidate
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = '__all__'
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter by college for multi-tenancy"""
        queryset = ScholarshipCandidate.objects.filter(is_deleted=False)

        # Filter by college if user is not superadmin
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)

        return queryset

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return ScholarshipCandidateListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ScholarshipCandidateCreateSerializer
        return ScholarshipCandidateDetailSerializer

    def perform_destroy(self, instance):
        """Soft delete"""
        instance.is_deleted = True
        instance.save()


class DonorViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Donor
    Provides CRUD operations for Donor
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = '__all__'
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter by college for multi-tenancy"""
        queryset = Donor.objects.filter(is_deleted=False)

        # Filter by college if user is not superadmin
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)

        return queryset

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return DonorListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return DonorCreateSerializer
        return DonorDetailSerializer

    def perform_destroy(self, instance):
        """Soft delete"""
        instance.is_deleted = True
        instance.save()


class ScholarshipViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Scholarship
    Provides CRUD operations for Scholarship
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = '__all__'
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter by college for multi-tenancy"""
        queryset = Scholarship.objects.filter(is_deleted=False)

        # Filter by college if user is not superadmin
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)

        return queryset

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return ScholarshipListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ScholarshipCreateSerializer
        return ScholarshipDetailSerializer

    def perform_destroy(self, instance):
        """Soft delete"""
        instance.is_deleted = True
        instance.save()

