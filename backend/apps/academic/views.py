"""Academic views"""
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
