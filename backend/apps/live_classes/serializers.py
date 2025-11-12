"""Live Class serializers"""
from rest_framework import serializers
from .models import LiveClassType, LiveClass, Assignment


class LiveClassTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiveClassType
        fields = '__all__'


class LiveClassSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(source='school_class.name', read_only=True)
    section_name = serializers.CharField(source='section.name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    teacher_name = serializers.CharField(source='teacher.user.get_full_name', read_only=True)
    live_class_type_name = serializers.CharField(source='live_class_type.name', read_only=True)

    class Meta:
        model = LiveClass
        fields = '__all__'


class AssignmentSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(source='school_class.name', read_only=True)
    section_name = serializers.CharField(source='section.name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)

    class Meta:
        model = Assignment
        fields = '__all__'
