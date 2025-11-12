"""Teacher views"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Teacher, TeacherLecture, Rating
from apps.colleges.models import Department
from .serializers import (DepartmentSerializer, TeacherListSerializer, TeacherDetailSerializer,
                          TeacherLectureSerializer, RatingSerializer)


class DepartmentViewSet(viewsets.ModelViewSet):
    """NOTE: This endpoint still works, but Department is now managed in colleges app"""
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
