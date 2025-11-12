"""Student serializers"""
from rest_framework import serializers
from .models import Student, StudentParent


class StudentListSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    class_name = serializers.CharField(source='school_class.name', read_only=True)
    section_name = serializers.CharField(source='section.name', read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'user_name', 'roll_number', 'class_name', 'section_name', 'photo', 'admission_date']


class StudentDetailSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    class_name = serializers.CharField(source='school_class.name', read_only=True)
    section_name = serializers.CharField(source='section.name', read_only=True)

    class Meta:
        model = Student
        fields = '__all__'

    def get_user(self, obj):
        return {
            'id': obj.user.id,
            'email': obj.user.email,
            'username': obj.user.username,
            'full_name': obj.user.get_full_name(),
            'phone': obj.user.phone,
        }


class StudentParentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    guardian_name = serializers.CharField(source='guardian.user.get_full_name', read_only=True)

    class Meta:
        model = StudentParent
        fields = '__all__'
