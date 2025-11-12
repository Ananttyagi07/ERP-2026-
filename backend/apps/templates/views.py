"""Template management views"""
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
