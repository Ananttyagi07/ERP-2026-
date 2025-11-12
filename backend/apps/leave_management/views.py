"""Leave Management views"""
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
