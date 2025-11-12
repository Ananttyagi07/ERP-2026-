"""
Serializers for frontend_cms
"""
from rest_framework import serializers
from .models import FrontendPage, Slider, AboutSchool


class FrontendPageListSerializer(serializers.ModelSerializer):
    """List serializer for FrontendPage"""

    class Meta:
        model = FrontendPage
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class FrontendPageCreateSerializer(serializers.ModelSerializer):
    """Create/Update serializer for FrontendPage"""

    class Meta:
        model = FrontendPage
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class FrontendPageDetailSerializer(serializers.ModelSerializer):
    """Detail serializer for FrontendPage"""

    class Meta:
        model = FrontendPage
        fields = '__all__'
        depth = 1


class SliderListSerializer(serializers.ModelSerializer):
    """List serializer for Slider"""

    class Meta:
        model = Slider
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class SliderCreateSerializer(serializers.ModelSerializer):
    """Create/Update serializer for Slider"""

    class Meta:
        model = Slider
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class SliderDetailSerializer(serializers.ModelSerializer):
    """Detail serializer for Slider"""

    class Meta:
        model = Slider
        fields = '__all__'
        depth = 1


class AboutSchoolListSerializer(serializers.ModelSerializer):
    """List serializer for AboutSchool"""

    class Meta:
        model = AboutSchool
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class AboutSchoolCreateSerializer(serializers.ModelSerializer):
    """Create/Update serializer for AboutSchool"""

    class Meta:
        model = AboutSchool
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class AboutSchoolDetailSerializer(serializers.ModelSerializer):
    """Detail serializer for AboutSchool"""

    class Meta:
        model = AboutSchool
        fields = '__all__'
        depth = 1


