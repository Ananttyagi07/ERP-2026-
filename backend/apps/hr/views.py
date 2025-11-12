"""HR views"""
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
