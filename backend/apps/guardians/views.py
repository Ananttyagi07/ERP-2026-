"""Guardian views"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Guardian
from .serializers import GuardianListSerializer, GuardianDetailSerializer


class GuardianViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Guardian.objects.select_related('user', 'college').all()

    def get_serializer_class(self):
        if self.action == 'list':
            return GuardianListSerializer
        return GuardianDetailSerializer
