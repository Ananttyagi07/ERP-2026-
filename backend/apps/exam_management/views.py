"""
Exam Management views
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Grade, ExamTerm, ExamSchedule, ExamSuggestion, ExamAttendanceRecord
from .serializers import *


class GradeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Grade.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return GradeListSerializer
        elif self.action in ['create', 'update']:
            return GradeCreateSerializer
        return GradeDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college, is_deleted=False)
        return queryset

    def perform_create(self, serializer):
        serializer.save(college=self.request.user.college)


class ExamTermViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ExamTerm.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ExamTermListSerializer
        elif self.action in ['create', 'update']:
            return ExamTermCreateSerializer
        return ExamTermDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college, is_deleted=False)
        return queryset

    def perform_create(self, serializer):
        serializer.save(college=self.request.user.college)


class ExamScheduleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ExamSchedule.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ExamScheduleListSerializer
        elif self.action in ['create', 'update']:
            return ExamScheduleCreateSerializer
        return ExamScheduleDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college, is_deleted=False)
        return queryset

    def perform_create(self, serializer):
        serializer.save(college=self.request.user.college)


class ExamSuggestionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ExamSuggestion.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ExamSuggestionListSerializer
        elif self.action in ['create', 'update']:
            return ExamSuggestionCreateSerializer
        return ExamSuggestionDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college, is_deleted=False)
        return queryset

    def perform_create(self, serializer):
        serializer.save(college=self.request.user.college)


class ExamAttendanceRecordViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ExamAttendanceRecord.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ExamAttendanceRecordListSerializer
        elif self.action in ['create', 'update']:
            return ExamAttendanceRecordCreateSerializer
        return ExamAttendanceRecordDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)
        return queryset

    def perform_create(self, serializer):
        serializer.save(college=self.request.user.college, marked_by=self.request.user)
