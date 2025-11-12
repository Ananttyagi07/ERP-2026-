"""
Certificate views
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import CertificateType, CertificateGeneration
from .serializers import *


class CertificateTypeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = CertificateType.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return CertificateTypeListSerializer
        elif self.action in ['create', 'update']:
            return CertificateTypeCreateSerializer
        return CertificateTypeDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college, is_deleted=False)
        return queryset

    def perform_create(self, serializer):
        serializer.save(college=self.request.user.college)


class CertificateGenerationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = CertificateGeneration.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return CertificateGenerationListSerializer
        elif self.action in ['create', 'update']:
            return CertificateGenerationCreateSerializer
        return CertificateGenerationDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)
        return queryset

    def perform_create(self, serializer):
        serializer.save(college=self.request.user.college, generated_by=self.request.user)
