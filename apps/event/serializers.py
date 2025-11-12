"""
Serializers for event
"""
from rest_framework import serializers
from .models import Event


class EventListSerializer(serializers.ModelSerializer):
    """List serializer for Event"""

    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class EventCreateSerializer(serializers.ModelSerializer):
    """Create/Update serializer for Event"""

    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class EventDetailSerializer(serializers.ModelSerializer):
    """Detail serializer for Event"""

    class Meta:
        model = Event
        fields = '__all__'
        depth = 1


