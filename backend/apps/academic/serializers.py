"""Academic serializers"""
from rest_framework import serializers
from .models import SchoolClass, ClassSection, Subject, Syllabus, StudyMaterial


class SchoolClassSerializer(serializers.ModelSerializer):
    class_teacher_name = serializers.CharField(source='class_teacher.user.get_full_name', read_only=True, allow_null=True)

    class Meta:
        model = SchoolClass
        fields = '__all__'


class ClassSectionSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(source='school_class.name', read_only=True)
    section_teacher_name = serializers.CharField(source='section_teacher.user.get_full_name', read_only=True, allow_null=True)

    class Meta:
        model = ClassSection
        fields = '__all__'


class SubjectSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(source='school_class.name', read_only=True)
    teacher_name = serializers.CharField(source='teacher.user.get_full_name', read_only=True, allow_null=True)

    class Meta:
        model = Subject
        fields = '__all__'


class SyllabusSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(source='school_class.name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)

    class Meta:
        model = Syllabus
        fields = '__all__'


class StudyMaterialSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(source='school_class.name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)

    class Meta:
        model = StudyMaterial
        fields = '__all__'
