"""
Online Exam views
"""
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import ExamInstruction, QuestionBank, OnlineExam, OnlineExamResult
from .serializers import *


class ExamInstructionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ExamInstruction.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ExamInstructionListSerializer
        elif self.action in ['create', 'update']:
            return ExamInstructionCreateSerializer
        return ExamInstructionDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college, is_deleted=False)
        return queryset

    def perform_create(self, serializer):
        serializer.save(college=self.request.user.college)


class QuestionBankViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = QuestionBank.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return QuestionBankListSerializer
        elif self.action in ['create', 'update']:
            return QuestionBankCreateSerializer
        return QuestionBankDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college, is_deleted=False)
        return queryset

    def perform_create(self, serializer):
        serializer.save(college=self.request.user.college)


class OnlineExamViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = OnlineExam.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return OnlineExamListSerializer
        elif self.action in ['create', 'update']:
            return OnlineExamCreateSerializer
        return OnlineExamDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college, is_deleted=False)
        return queryset

    def perform_create(self, serializer):
        serializer.save(college=self.request.user.college)

    @action(detail=True, methods=['post'], url_path='publish')
    def publish(self, request, pk=None):
        exam = self.get_object()
        exam.publish_status = True
        exam.save()
        return Response({'success': True, 'message': 'Exam published successfully'})


class OnlineExamResultViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = OnlineExamResult.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return OnlineExamResultListSerializer
        elif self.action in ['create', 'update']:
            return OnlineExamResultCreateSerializer
        return OnlineExamResultDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)
        return queryset

    def perform_create(self, serializer):
        serializer.save(college=self.request.user.college)
