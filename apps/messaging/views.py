"""
Views for messaging
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Message
from .serializers import (
    MessageListSerializer, MessageCreateSerializer, MessageDetailSerializer,
)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Message
    Provides CRUD operations for Message
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = '__all__'
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter by college for multi-tenancy"""
        queryset = Message.objects.filter(is_deleted=False)

        # Filter by college if user is not superadmin
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)

        return queryset

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return MessageListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return MessageCreateSerializer
        return MessageDetailSerializer

    def perform_destroy(self, instance):
        """Soft delete"""
        instance.is_deleted = True
        instance.save()

