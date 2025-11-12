"""Superadmin management views"""
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
