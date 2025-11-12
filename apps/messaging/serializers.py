"""
Serializers for messaging
"""
from rest_framework import serializers
from .models import Message


class MessageListSerializer(serializers.ModelSerializer):
    """List serializer for Message"""

    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class MessageCreateSerializer(serializers.ModelSerializer):
    """Create/Update serializer for Message"""

    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class MessageDetailSerializer(serializers.ModelSerializer):
    """Detail serializer for Message"""

    class Meta:
        model = Message
        fields = '__all__'
        depth = 1


