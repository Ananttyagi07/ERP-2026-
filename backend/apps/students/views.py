"""Student views"""
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
