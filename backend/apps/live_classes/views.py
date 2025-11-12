"""Live Class views"""
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
