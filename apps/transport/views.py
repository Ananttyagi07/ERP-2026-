"""
Views for transport
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Vehicle, TransportRoute, RouteStop, TransportMember
from .serializers import (
    VehicleListSerializer, VehicleCreateSerializer, VehicleDetailSerializer,
    TransportRouteListSerializer, TransportRouteCreateSerializer, TransportRouteDetailSerializer,
    RouteStopListSerializer, RouteStopCreateSerializer, RouteStopDetailSerializer,
    TransportMemberListSerializer, TransportMemberCreateSerializer, TransportMemberDetailSerializer,
)


class VehicleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Vehicle
    Provides CRUD operations for Vehicle
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = '__all__'
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter by college for multi-tenancy"""
        queryset = Vehicle.objects.filter(is_deleted=False)

        # Filter by college if user is not superadmin
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)

        return queryset

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return VehicleListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return VehicleCreateSerializer
        return VehicleDetailSerializer

    def perform_destroy(self, instance):
        """Soft delete"""
        instance.is_deleted = True
        instance.save()


class TransportRouteViewSet(viewsets.ModelViewSet):
    """
    ViewSet for TransportRoute
    Provides CRUD operations for TransportRoute
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = '__all__'
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter by college for multi-tenancy"""
        queryset = TransportRoute.objects.filter(is_deleted=False)

        # Filter by college if user is not superadmin
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)

        return queryset

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return TransportRouteListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return TransportRouteCreateSerializer
        return TransportRouteDetailSerializer

    def perform_destroy(self, instance):
        """Soft delete"""
        instance.is_deleted = True
        instance.save()


class RouteStopViewSet(viewsets.ModelViewSet):
    """
    ViewSet for RouteStop
    Provides CRUD operations for RouteStop
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = '__all__'
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter by college for multi-tenancy"""
        queryset = RouteStop.objects.filter(is_deleted=False)

        # Filter by college if user is not superadmin
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)

        return queryset

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return RouteStopListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return RouteStopCreateSerializer
        return RouteStopDetailSerializer

    def perform_destroy(self, instance):
        """Soft delete"""
        instance.is_deleted = True
        instance.save()


class TransportMemberViewSet(viewsets.ModelViewSet):
    """
    ViewSet for TransportMember
    Provides CRUD operations for TransportMember
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = '__all__'
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter by college for multi-tenancy"""
        queryset = TransportMember.objects.filter(is_deleted=False)

        # Filter by college if user is not superadmin
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)

        return queryset

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return TransportMemberListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return TransportMemberCreateSerializer
        return TransportMemberDetailSerializer

    def perform_destroy(self, instance):
        """Soft delete"""
        instance.is_deleted = True
        instance.save()

