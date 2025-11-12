"""
Views for library
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Book, LibraryMember, BookIssue, EBook
from .serializers import (
    BookListSerializer, BookCreateSerializer, BookDetailSerializer,
    LibraryMemberListSerializer, LibraryMemberCreateSerializer, LibraryMemberDetailSerializer,
    BookIssueListSerializer, BookIssueCreateSerializer, BookIssueDetailSerializer,
    EBookListSerializer, EBookCreateSerializer, EBookDetailSerializer,
)


class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Book
    Provides CRUD operations for Book
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = '__all__'
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter by college for multi-tenancy"""
        queryset = Book.objects.filter(is_deleted=False)

        # Filter by college if user is not superadmin
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)

        return queryset

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return BookListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return BookCreateSerializer
        return BookDetailSerializer

    def perform_destroy(self, instance):
        """Soft delete"""
        instance.is_deleted = True
        instance.save()


class LibraryMemberViewSet(viewsets.ModelViewSet):
    """
    ViewSet for LibraryMember
    Provides CRUD operations for LibraryMember
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = '__all__'
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter by college for multi-tenancy"""
        queryset = LibraryMember.objects.filter(is_deleted=False)

        # Filter by college if user is not superadmin
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)

        return queryset

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return LibraryMemberListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return LibraryMemberCreateSerializer
        return LibraryMemberDetailSerializer

    def perform_destroy(self, instance):
        """Soft delete"""
        instance.is_deleted = True
        instance.save()


class BookIssueViewSet(viewsets.ModelViewSet):
    """
    ViewSet for BookIssue
    Provides CRUD operations for BookIssue
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = '__all__'
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter by college for multi-tenancy"""
        queryset = BookIssue.objects.filter(is_deleted=False)

        # Filter by college if user is not superadmin
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)

        return queryset

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return BookIssueListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return BookIssueCreateSerializer
        return BookIssueDetailSerializer

    def perform_destroy(self, instance):
        """Soft delete"""
        instance.is_deleted = True
        instance.save()


class EBookViewSet(viewsets.ModelViewSet):
    """
    ViewSet for EBook
    Provides CRUD operations for EBook
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = '__all__'
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter by college for multi-tenancy"""
        queryset = EBook.objects.filter(is_deleted=False)

        # Filter by college if user is not superadmin
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)

        return queryset

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return EBookListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return EBookCreateSerializer
        return EBookDetailSerializer

    def perform_destroy(self, instance):
        """Soft delete"""
        instance.is_deleted = True
        instance.save()

