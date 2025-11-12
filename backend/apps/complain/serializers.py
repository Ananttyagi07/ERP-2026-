"""
Serializers for complain
"""
from rest_framework import serializers
from .models import ComplainType, Complain


class ComplainTypeListSerializer(serializers.ModelSerializer):
    """List serializer for ComplainType"""

    class Meta:
        model = ComplainType
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class ComplainTypeCreateSerializer(serializers.ModelSerializer):
    """Create/Update serializer for ComplainType"""

    class Meta:
        model = ComplainType
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class ComplainTypeDetailSerializer(serializers.ModelSerializer):
    """Detail serializer for ComplainType"""

    class Meta:
        model = ComplainType
        fields = '__all__'
        depth = 1


class ComplainListSerializer(serializers.ModelSerializer):
    """List serializer for Complain"""

    class Meta:
        model = Complain
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class ComplainCreateSerializer(serializers.ModelSerializer):
    """Create/Update serializer for Complain"""

    class Meta:
        model = Complain
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class ComplainDetailSerializer(serializers.ModelSerializer):
    """Detail serializer for Complain"""

    class Meta:
        model = Complain
        fields = '__all__'
        depth = 1


