#!/usr/bin/env python3
"""Generate all ViewSets for ERP modules"""

VIEWS_FILES = {
    'apps/superadmin/views.py': '''"""Superadmin management views"""
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import SuperAdminProfile
from .serializers import SuperAdminListSerializer, SuperAdminDetailSerializer, SuperAdminCreateSerializer


class SuperAdminViewSet(viewsets.ModelViewSet):
    """Superadmin CRUD operations"""
    permission_classes = [IsAuthenticated]
    queryset = SuperAdminProfile.objects.select_related('user', 'college').all()

    def get_serializer_class(self):
        if self.action == 'list':
            return SuperAdminListSerializer
        elif self.action == 'create':
            return SuperAdminCreateSerializer
        return SuperAdminDetailSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({'success': True, 'message': 'Superadmin created successfully', 'data': serializer.data}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = SuperAdminDetailSerializer(instance, data=request.data, partial=kwargs.get('partial', False))
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({'success': True, 'message': 'Superadmin updated successfully', 'data': serializer.data}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.soft_delete()
        return Response({'success': True, 'message': 'Superadmin deleted successfully'}, status=status.HTTP_200_OK)
''',

    'apps/templates/views.py': '''"""Template management views"""
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import SMSTemplate, EmailTemplate
from .serializers import SMSTemplateSerializer, EmailTemplateSerializer


class SMSTemplateViewSet(viewsets.ModelViewSet):
    """SMS Template CRUD"""
    permission_classes = [IsAuthenticated]
    queryset = SMSTemplate.objects.all()
    serializer_class = SMSTemplateSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)


class EmailTemplateViewSet(viewsets.ModelViewSet):
    """Email Template CRUD"""
    permission_classes = [IsAuthenticated]
    queryset = EmailTemplate.objects.all()
    serializer_class = EmailTemplateSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
''',

    'apps/front_office/views.py': '''"""Front Office views"""
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import VisitorPurpose, VisitorInfo, CallLog, PostalDispatch, PostalReceive
from .serializers import (VisitorPurposeSerializer, VisitorInfoSerializer, CallLogSerializer,
                          PostalDispatchSerializer, PostalReceiveSerializer)


class VisitorPurposeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = VisitorPurpose.objects.all()
    serializer_class = VisitorPurposeSerializer


class VisitorInfoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = VisitorInfo.objects.select_related('purpose', 'meet_staff_id', 'college').all()
    serializer_class = VisitorInfoSerializer


class CallLogViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = CallLog.objects.all()
    serializer_class = CallLogSerializer


class PostalDispatchViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = PostalDispatch.objects.all()
    serializer_class = PostalDispatchSerializer


class PostalReceiveViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = PostalReceive.objects.all()
    serializer_class = PostalReceiveSerializer
''',

    'apps/hr/views.py': '''"""HR views"""
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Designation, Employee
from .serializers import DesignationSerializer, EmployeeListSerializer, EmployeeDetailSerializer


class DesignationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Employee.objects.select_related('user', 'designation', 'college').all()

    def get_serializer_class(self):
        if self.action == 'list':
            return EmployeeListSerializer
        return EmployeeDetailSerializer
''',

    'apps/teachers/views.py': '''"""Teacher views"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Department, Teacher, TeacherLecture, Rating
from .serializers import (DepartmentSerializer, TeacherListSerializer, TeacherDetailSerializer,
                          TeacherLectureSerializer, RatingSerializer)


class DepartmentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Department.objects.select_related('college', 'head').all()
    serializer_class = DepartmentSerializer


class TeacherViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Teacher.objects.select_related('user', 'department', 'designation', 'college').all()

    def get_serializer_class(self):
        if self.action == 'list':
            return TeacherListSerializer
        return TeacherDetailSerializer


class TeacherLectureViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = TeacherLecture.objects.select_related('teacher', 'class_id', 'section_id', 'subject_id', 'college').all()
    serializer_class = TeacherLectureSerializer


class RatingViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Rating.objects.select_related('teacher', 'department', 'rated_by', 'college').all()
    serializer_class = RatingSerializer
''',

    'apps/leave_management/views.py': '''"""Leave Management views"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import LeaveType, LeaveApplication
from .serializers import LeaveTypeSerializer, LeaveApplicationSerializer


class LeaveTypeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = LeaveType.objects.all()
    serializer_class = LeaveTypeSerializer


class LeaveApplicationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = LeaveApplication.objects.select_related('leave_type', 'applicant', 'approved_by', 'college').all()
    serializer_class = LeaveApplicationSerializer

    @action(detail=False, methods=['get'])
    def waiting(self, request):
        """Get waiting/pending applications"""
        queryset = self.get_queryset().filter(status='Pending')
        serializer = self.get_serializer(queryset, many=True)
        return Response({'success': True, 'data': serializer.data})

    @action(detail=False, methods=['get'])
    def approved(self, request):
        """Get approved applications"""
        queryset = self.get_queryset().filter(status='Approved')
        serializer = self.get_serializer(queryset, many=True)
        return Response({'success': True, 'data': serializer.data})

    @action(detail=False, methods=['get'])
    def declined(self, request):
        """Get declined applications"""
        queryset = self.get_queryset().filter(status='Declined')
        serializer = self.get_serializer(queryset, many=True)
        return Response({'success': True, 'data': serializer.data})

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve leave application"""
        application = self.get_object()
        application.status = 'Approved'
        application.approved_by = request.user
        application.approval_date = timezone.now()
        application.approval_note = request.data.get('approval_note', '')
        application.save()
        return Response({'success': True, 'message': 'Leave application approved'})

    @action(detail=True, methods=['post'])
    def decline(self, request, pk=None):
        """Decline leave application"""
        application = self.get_object()
        application.status = 'Declined'
        application.approved_by = request.user
        application.approval_date = timezone.now()
        application.approval_note = request.data.get('approval_note', '')
        application.save()
        return Response({'success': True, 'message': 'Leave application declined'})
''',

    'apps/academic/views.py': '''"""Academic views"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import SchoolClass, ClassSection, Subject, Syllabus, StudyMaterial
from .serializers import (SchoolClassSerializer, ClassSectionSerializer, SubjectSerializer,
                          SyllabusSerializer, StudyMaterialSerializer)


class SchoolClassViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = SchoolClass.objects.select_related('college', 'class_teacher').all()
    serializer_class = SchoolClassSerializer


class ClassSectionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ClassSection.objects.select_related('school_class', 'section_teacher', 'college').all()
    serializer_class = ClassSectionSerializer


class SubjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Subject.objects.select_related('school_class', 'teacher', 'college').all()
    serializer_class = SubjectSerializer


class SyllabusViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Syllabus.objects.select_related('school_class', 'subject', 'college').all()
    serializer_class = SyllabusSerializer


class StudyMaterialViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = StudyMaterial.objects.select_related('school_class', 'subject', 'college').all()
    serializer_class = StudyMaterialSerializer
''',

    'apps/live_classes/views.py': '''"""Live Class views"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import LiveClassType, LiveClass, Assignment
from .serializers import LiveClassTypeSerializer, LiveClassSerializer, AssignmentSerializer


class LiveClassTypeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = LiveClassType.objects.all()
    serializer_class = LiveClassTypeSerializer


class LiveClassViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = LiveClass.objects.select_related('school_class', 'section', 'subject', 'teacher', 'live_class_type', 'college').all()
    serializer_class = LiveClassSerializer


class AssignmentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Assignment.objects.select_related('school_class', 'section', 'subject', 'college').all()
    serializer_class = AssignmentSerializer
''',

    'apps/students/views.py': '''"""Student views"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Student, StudentParent
from .serializers import StudentListSerializer, StudentDetailSerializer, StudentParentSerializer


class StudentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Student.objects.select_related('user', 'school_class', 'section', 'college').all()

    def get_serializer_class(self):
        if self.action == 'list':
            return StudentListSerializer
        return StudentDetailSerializer


class StudentParentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = StudentParent.objects.select_related('student', 'guardian').all()
    serializer_class = StudentParentSerializer
''',

    'apps/guardians/views.py': '''"""Guardian views"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Guardian
from .serializers import GuardianListSerializer, GuardianDetailSerializer


class GuardianViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Guardian.objects.select_related('user', 'college').all()

    def get_serializer_class(self):
        if self.action == 'list':
            return GuardianListSerializer
        return GuardianDetailSerializer
''',
}

print("🚀 Generating ViewSets...")
print("=" * 60)

for filepath, content in VIEWS_FILES.items():
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"✓ {filepath}")

print("\n✅ All ViewSets created!")
print("=" * 60)
