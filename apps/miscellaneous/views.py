"""
Views for miscellaneous
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Award, Todo, FAQ
from .serializers import (
    AwardListSerializer, AwardCreateSerializer, AwardDetailSerializer,
    TodoListSerializer, TodoCreateSerializer, TodoDetailSerializer,
    FAQListSerializer, FAQCreateSerializer, FAQDetailSerializer,
)


class AwardViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Award
    Provides CRUD operations for Award
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = '__all__'
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter by college for multi-tenancy"""
        queryset = Award.objects.filter(is_deleted=False)

        # Filter by college if user is not superadmin
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)

        return queryset

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return AwardListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return AwardCreateSerializer
        return AwardDetailSerializer

    def perform_destroy(self, instance):
        """Soft delete"""
        instance.is_deleted = True
        instance.save()


class TodoViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Todo
    Provides CRUD operations for Todo
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = '__all__'
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter by college for multi-tenancy"""
        queryset = Todo.objects.filter(is_deleted=False)

        # Filter by college if user is not superadmin
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)

        return queryset

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return TodoListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return TodoCreateSerializer
        return TodoDetailSerializer

    def perform_destroy(self, instance):
        """Soft delete"""
        instance.is_deleted = True
        instance.save()


class FAQViewSet(viewsets.ModelViewSet):
    """
    ViewSet for FAQ
    Provides CRUD operations for FAQ
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = '__all__'
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter by college for multi-tenancy"""
        queryset = FAQ.objects.filter(is_deleted=False)

        # Filter by college if user is not superadmin
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)

        return queryset

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return FAQListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return FAQCreateSerializer
        return FAQDetailSerializer

    def perform_destroy(self, instance):
        """Soft delete"""
        instance.is_deleted = True
        instance.save()

