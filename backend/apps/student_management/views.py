"""
Student Management views
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import StudentType, OnlineAdmission, StudentActivity
from .serializers import (
    StudentTypeListSerializer, StudentTypeCreateSerializer, StudentTypeDetailSerializer,
    OnlineAdmissionListSerializer, OnlineAdmissionCreateSerializer, OnlineAdmissionDetailSerializer,
    StudentActivityListSerializer, StudentActivityCreateSerializer, StudentActivityDetailSerializer
)


class StudentTypeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing student types
    """
    permission_classes = [IsAuthenticated]
    queryset = StudentType.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return StudentTypeListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return StudentTypeCreateSerializer
        return StudentTypeDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college, is_deleted=False)
        return queryset

    def perform_create(self, serializer):
        serializer.save(college=self.request.user.college)


class OnlineAdmissionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing online admissions
    """
    permission_classes = [IsAuthenticated]
    queryset = OnlineAdmission.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return OnlineAdmissionListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return OnlineAdmissionCreateSerializer
        return OnlineAdmissionDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college, is_deleted=False)

        # Filter by status
        status_param = self.request.query_params.get('status')
        if status_param:
            queryset = queryset.filter(status=status_param)

        return queryset

    def perform_create(self, serializer):
        serializer.save(college=self.request.user.college)

    @action(detail=True, methods=['post'], url_path='approve')
    def approve(self, request, pk=None):
        admission = self.get_object()
        admission.status = 'Approved'
        admission.save()
        return Response({
            'success': True,
            'message': 'Admission approved successfully'
        })

    @action(detail=True, methods=['post'], url_path='reject')
    def reject(self, request, pk=None):
        admission = self.get_object()
        admission.status = 'Rejected'
        admission.save()
        return Response({
            'success': True,
            'message': 'Admission rejected'
        })


class StudentActivityViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing student activities
    """
    permission_classes = [IsAuthenticated]
    queryset = StudentActivity.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return StudentActivityListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return StudentActivityCreateSerializer
        return StudentActivityDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college, is_deleted=False)

        # Filter by student
        student_id = self.request.query_params.get('student_id')
        if student_id:
            queryset = queryset.filter(student_id=student_id)

        # Filter by class
        class_id = self.request.query_params.get('class_id')
        if class_id:
            queryset = queryset.filter(school_class_id=class_id)

        return queryset

    def perform_create(self, serializer):
        serializer.save(college=self.request.user.college)
