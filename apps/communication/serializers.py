"""
Serializers for communication
"""
from rest_framework import serializers
from .models import EmailLog, SMSLog


class EmailLogListSerializer(serializers.ModelSerializer):
    """List serializer for EmailLog"""

    class Meta:
        model = EmailLog
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class EmailLogCreateSerializer(serializers.ModelSerializer):
    """Create/Update serializer for EmailLog"""

    class Meta:
        model = EmailLog
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class EmailLogDetailSerializer(serializers.ModelSerializer):
    """Detail serializer for EmailLog"""

    class Meta:
        model = EmailLog
        fields = '__all__'
        depth = 1


class SMSLogListSerializer(serializers.ModelSerializer):
    """List serializer for SMSLog"""

    class Meta:
        model = SMSLog
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class SMSLogCreateSerializer(serializers.ModelSerializer):
    """Create/Update serializer for SMSLog"""

    class Meta:
        model = SMSLog
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class SMSLogDetailSerializer(serializers.ModelSerializer):
    """Detail serializer for SMSLog"""

    class Meta:
        model = SMSLog
        fields = '__all__'
        depth = 1


