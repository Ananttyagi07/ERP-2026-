"""
Student Management serializers
"""
from rest_framework import serializers
from .models import StudentType, OnlineAdmission, StudentActivity


class StudentTypeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentType
        fields = ['id', 'name', 'note', 'created_at']


class StudentTypeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentType
        fields = ['name', 'note']


class StudentTypeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentType
        fields = '__all__'


class OnlineAdmissionListSerializer(serializers.ModelSerializer):
    school_class_name = serializers.CharField(source='school_class.name', read_only=True)

    class Meta:
        model = OnlineAdmission
        fields = ['id', 'student_name', 'email', 'phone', 'school_class_name', 'status', 'created_at']


class OnlineAdmissionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnlineAdmission
        fields = ['student_name', 'email', 'phone', 'school_class', 'photo', 'application_data']


class OnlineAdmissionDetailSerializer(serializers.ModelSerializer):
    school_class_name = serializers.CharField(source='school_class.name', read_only=True)

    class Meta:
        model = OnlineAdmission
        fields = '__all__'


class StudentActivityListSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    class_name = serializers.CharField(source='school_class.name', read_only=True)
    section_name = serializers.CharField(source='section.name', read_only=True)

    class Meta:
        model = StudentActivity
        fields = ['id', 'student_name', 'class_name', 'section_name', 'activity', 'activity_date']


class StudentActivityCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentActivity
        fields = ['student', 'school_class', 'section', 'activity', 'activity_date']


class StudentActivityDetailSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    class_name = serializers.CharField(source='school_class.name', read_only=True)
    section_name = serializers.CharField(source='section.name', read_only=True)

    class Meta:
        model = StudentActivity
        fields = '__all__'
