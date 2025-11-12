"""Front Office views"""
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
