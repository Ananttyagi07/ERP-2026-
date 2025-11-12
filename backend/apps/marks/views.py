"""
Marks Management views
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import ExamMark, MarkDistribution, ResultCard, MarkEmailLog, MarkSMSLog, ResultEmailLog, ResultSMSLog
from .serializers import *


class ExamMarkViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ExamMark.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ExamMarkListSerializer
        elif self.action in ['create', 'update']:
            return ExamMarkCreateSerializer
        return ExamMarkDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college, is_deleted=False)
        return queryset

    def perform_create(self, serializer):
        serializer.save(college=self.request.user.college)


class MarkDistributionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = MarkDistribution.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return MarkDistributionListSerializer
        elif self.action in ['create', 'update']:
            return MarkDistributionCreateSerializer
        return MarkDistributionDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college, is_deleted=False)
        return queryset

    def perform_create(self, serializer):
        serializer.save(college=self.request.user.college)


class ResultCardViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ResultCard.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ResultCardListSerializer
        return ResultCardDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)
        return queryset


class MarkEmailLogViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = MarkEmailLog.objects.all()
    serializer_class = MarkEmailLogSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)
        return queryset


class MarkSMSLogViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = MarkSMSLog.objects.all()
    serializer_class = MarkSMSLogSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)
        return queryset


class ResultEmailLogViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ResultEmailLog.objects.all()
    serializer_class = ResultEmailLogSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)
        return queryset


class ResultSMSLogViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ResultSMSLog.objects.all()
    serializer_class = ResultSMSLogSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)
        return queryset
