"""
Attendance views
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import (
    StudentAttendance, TeacherAttendance, EmployeeAttendance,
    AbsentEmailLog, AbsentSMSLog
)
from .serializers import (
    StudentAttendanceListSerializer, StudentAttendanceCreateSerializer,
    TeacherAttendanceListSerializer, TeacherAttendanceCreateSerializer,
    EmployeeAttendanceListSerializer, EmployeeAttendanceCreateSerializer,
    AbsentEmailLogSerializer, AbsentSMSLogSerializer
)


class StudentAttendanceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for student attendance management
    """
    permission_classes = [IsAuthenticated]
    queryset = StudentAttendance.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return StudentAttendanceListSerializer
        return StudentAttendanceCreateSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)

        # Filter by date
        date = self.request.query_params.get('date')
        if date:
            queryset = queryset.filter(attendance_date=date)

        # Filter by class
        class_id = self.request.query_params.get('class_id')
        if class_id:
            queryset = queryset.filter(school_class_id=class_id)

        # Filter by section
        section_id = self.request.query_params.get('section_id')
        if section_id:
            queryset = queryset.filter(section_id=section_id)

        return queryset

    def perform_create(self, serializer):
        serializer.save(
            college=self.request.user.college,
            marked_by=self.request.user
        )


class TeacherAttendanceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for teacher attendance management
    """
    permission_classes = [IsAuthenticated]
    queryset = TeacherAttendance.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return TeacherAttendanceListSerializer
        return TeacherAttendanceCreateSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)

        # Filter by date
        date = self.request.query_params.get('date')
        if date:
            queryset = queryset.filter(attendance_date=date)

        return queryset

    def perform_create(self, serializer):
        serializer.save(
            college=self.request.user.college,
            marked_by=self.request.user
        )


class EmployeeAttendanceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for employee attendance management
    """
    permission_classes = [IsAuthenticated]
    queryset = EmployeeAttendance.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return EmployeeAttendanceListSerializer
        return EmployeeAttendanceCreateSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)

        # Filter by date
        date = self.request.query_params.get('date')
        if date:
            queryset = queryset.filter(attendance_date=date)

        return queryset

    def perform_create(self, serializer):
        serializer.save(
            college=self.request.user.college,
            marked_by=self.request.user
        )


class AbsentEmailLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for absent email logs (read-only)
    """
    permission_classes = [IsAuthenticated]
    queryset = AbsentEmailLog.objects.all()
    serializer_class = AbsentEmailLogSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)
        return queryset


class AbsentSMSLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for absent SMS logs (read-only)
    """
    permission_classes = [IsAuthenticated]
    queryset = AbsentSMSLog.objects.all()
    serializer_class = AbsentSMSLogSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)
        return queryset
