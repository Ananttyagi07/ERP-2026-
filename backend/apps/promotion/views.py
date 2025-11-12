"""
Promotion views
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import StudentPromotion
from .serializers import *


class StudentPromotionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = StudentPromotion.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return StudentPromotionListSerializer
        elif self.action in ['create', 'update']:
            return StudentPromotionCreateSerializer
        return StudentPromotionDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)
        return queryset

    def perform_create(self, serializer):
        serializer.save(college=self.request.user.college, promoted_by=self.request.user)
