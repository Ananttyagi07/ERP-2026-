"""Teacher serializers"""
from rest_framework import serializers
from .models import Teacher, TeacherLecture, Rating
from apps.colleges.models import Department


class DepartmentSerializer(serializers.ModelSerializer):
    head_name = serializers.CharField(source='head.get_full_name', read_only=True, allow_null=True)

    class Meta:
        model = Department
        fields = '__all__'


class TeacherListSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)

    class Meta:
        model = Teacher
        fields = ['id', 'user_name', 'department_name', 'designation', 'joining_date', 'photo']


class TeacherDetailSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    department_name = serializers.CharField(source='department.name', read_only=True)

    class Meta:
        model = Teacher
        fields = '__all__'

    def get_user(self, obj):
        return {
            'id': obj.user.id,
            'email': obj.user.email,
            'username': obj.user.username,
            'full_name': obj.user.get_full_name(),
            'phone': obj.user.phone,
        }


class TeacherLectureSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.user.get_full_name', read_only=True)
    class_name = serializers.CharField(source='class_id.name', read_only=True)
    section_name = serializers.CharField(source='section_id.name', read_only=True)
    subject_name = serializers.CharField(source='subject_id.name', read_only=True)

    class Meta:
        model = TeacherLecture
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.user.get_full_name', read_only=True, allow_null=True)
    department_name = serializers.CharField(source='department.name', read_only=True, allow_null=True)
    rated_by_name = serializers.CharField(source='rated_by.get_full_name', read_only=True, allow_null=True)

    class Meta:
        model = Rating
        fields = '__all__'
