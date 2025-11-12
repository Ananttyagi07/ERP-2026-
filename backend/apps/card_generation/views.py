"""
Card Generation views
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import IDCardSetting, AdmitCardSetting
from .serializers import IDCardSettingSerializer, AdmitCardSettingSerializer


class IDCardSettingViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = IDCardSetting.objects.all()
    serializer_class = IDCardSettingSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college, is_deleted=False)
        return queryset

    def perform_create(self, serializer):
        serializer.save(college=self.request.user.college)


class AdmitCardSettingViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = AdmitCardSetting.objects.all()
    serializer_class = AdmitCardSettingSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college, is_deleted=False)
        return queryset

    def perform_create(self, serializer):
        serializer.save(college=self.request.user.college)
