"""
Certificate Generation serializers
"""
from rest_framework import serializers
from .models import CertificateType, CertificateGeneration


class CertificateTypeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CertificateType
        fields = ['id', 'certificate_name', 'school_name', 'created_at']


class CertificateTypeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CertificateType
        fields = [
            'certificate_name', 'school_name', 'certificate_text',
            'footer_left_text', 'footer_middle_text', 'footer_right_text', 'background'
        ]


class CertificateTypeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CertificateType
        fields = '__all__'


class CertificateGenerationListSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    certificate_type_name = serializers.CharField(source='certificate_type.certificate_name', read_only=True)
    class_name = serializers.CharField(source='school_class.name', read_only=True)

    class Meta:
        model = CertificateGeneration
        fields = [
            'id', 'certificate_type_name', 'student_name', 'class_name', 'created_at'
        ]


class CertificateGenerationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CertificateGeneration
        fields = ['certificate_type', 'student', 'school_class', 'section']


class CertificateGenerationDetailSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    certificate_type_name = serializers.CharField(source='certificate_type.certificate_name', read_only=True)
    class_name = serializers.CharField(source='school_class.name', read_only=True)
    section_name = serializers.CharField(source='section.name', read_only=True)

    class Meta:
        model = CertificateGeneration
        fields = '__all__'
