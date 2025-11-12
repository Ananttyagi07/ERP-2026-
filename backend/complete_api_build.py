#!/usr/bin/env python3
"""
Complete API Build Script
Generates all serializers, views, URLs, and admin for 10 modules
"""
import os

print("🚀 Starting Complete API Build...")
print("=" * 60)

# ============================================================================
# SERIALIZERS
# ============================================================================

SERIALIZERS_FILES = {
    'apps/superadmin/serializers.py': '''"""Superadmin serializers"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import SuperAdminProfile
from apps.roles.models import Role
from apps.users.models import UserRoleAssignment

User = get_user_model()


class SuperAdminListSerializer(serializers.ModelSerializer):
    """List serializer"""
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    user_phone = serializers.CharField(source='user.phone', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)

    class Meta:
        model = SuperAdminProfile
        fields = ['id', 'user_id', 'user_email', 'user_name', 'user_phone', 'photo', 'national_id', 'created_at']


class SuperAdminDetailSerializer(serializers.ModelSerializer):
    """Detail serializer"""
    user = serializers.SerializerMethodField()

    class Meta:
        model = SuperAdminProfile
        fields = '__all__'

    def get_user(self, obj):
        return {
            'id': obj.user.id,
            'email': obj.user.email,
            'username': obj.user.username,
            'first_name': obj.user.first_name,
            'last_name': obj.user.last_name,
            'phone': obj.user.phone,
            'gender': getattr(obj.user, 'gender', ''),
        }


class SuperAdminCreateSerializer(serializers.Serializer):
    """Create serializer"""
    # User fields
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    gender = serializers.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female')], required=True)
    college_id = serializers.IntegerField(required=True)

    # Profile fields
    national_id = serializers.CharField(required=False, allow_blank=True)
    blood_group = serializers.CharField(required=False, allow_blank=True)
    religion = serializers.CharField(required=False, allow_blank=True)
    birth_date = serializers.DateField(required=False, allow_null=True)
    present_address = serializers.CharField(required=False, allow_blank=True)
    permanent_address = serializers.CharField(required=False, allow_blank=True)
    resume = serializers.FileField(required=False, allow_null=True)
    photo = serializers.ImageField(required=False, allow_null=True)
    other_info = serializers.CharField(required=False, allow_blank=True)

    def create(self, validated_data):
        # Extract user fields
        user_data = {
            'email': validated_data.pop('email'),
            'username': validated_data.pop('username'),
            'first_name': validated_data.pop('first_name'),
            'last_name': validated_data.pop('last_name'),
            'phone': validated_data.pop('phone'),
            'college_id': validated_data.pop('college_id'),
        }
        password = validated_data.pop('password')
        gender = validated_data.pop('gender', '')

        # Create user
        user = User.objects.create_user(**user_data, password=password)
        if gender:
            user.gender = gender
            user.save()

        # Assign Superadmin role
        try:
            superadmin_role = Role.objects.get(name='Superadmin')
            UserRoleAssignment.objects.create(
                user=user,
                role=superadmin_role,
                college=user.college,
                is_active=True
            )
        except Role.DoesNotExist:
            pass

        # Create profile
        profile = SuperAdminProfile.objects.create(user=user, college=user.college, **validated_data)
        return profile
''',

    'apps/templates/serializers.py': '''"""Template serializers"""
from rest_framework import serializers
from .models import SMSTemplate, EmailTemplate


class SMSTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMSTemplate
        fields = '__all__'


class EmailTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailTemplate
        fields = '__all__'
''',

    'apps/front_office/serializers.py': '''"""Front Office serializers"""
from rest_framework import serializers
from .models import VisitorPurpose, VisitorInfo, CallLog, PostalDispatch, PostalReceive


class VisitorPurposeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitorPurpose
        fields = '__all__'


class VisitorInfoSerializer(serializers.ModelSerializer):
    purpose_name = serializers.CharField(source='purpose.purpose', read_only=True)
    meet_staff_name = serializers.CharField(source='meet_staff_id.get_full_name', read_only=True, allow_null=True)

    class Meta:
        model = VisitorInfo
        fields = '__all__'


class CallLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallLog
        fields = '__all__'


class PostalDispatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostalDispatch
        fields = '__all__'


class PostalReceiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostalReceive
        fields = '__all__'
''',

    'apps/hr/serializers.py': '''"""HR serializers"""
from rest_framework import serializers
from .models import Designation, Employee


class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = '__all__'


class EmployeeListSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    designation_name = serializers.CharField(source='designation.name', read_only=True)

    class Meta:
        model = Employee
        fields = ['id', 'user_name', 'designation_name', 'joining_date', 'photo']


class EmployeeDetailSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    designation_name = serializers.CharField(source='designation.name', read_only=True)

    class Meta:
        model = Employee
        fields = '__all__'

    def get_user(self, obj):
        return {
            'id': obj.user.id,
            'email': obj.user.email,
            'username': obj.user.username,
            'full_name': obj.user.get_full_name(),
            'phone': obj.user.phone,
        }
''',

    'apps/teachers/serializers.py': '''"""Teacher serializers"""
from rest_framework import serializers
from .models import Department, Teacher, TeacherLecture, Rating


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
''',

    'apps/leave_management/serializers.py': '''"""Leave Management serializers"""
from rest_framework import serializers
from .models import LeaveType, LeaveApplication


class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = '__all__'


class LeaveApplicationSerializer(serializers.ModelSerializer):
    applicant_name = serializers.CharField(source='applicant.get_full_name', read_only=True)
    leave_type_name = serializers.CharField(source='leave_type.name', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.get_full_name', read_only=True, allow_null=True)
    total_days = serializers.ReadOnlyField()

    class Meta:
        model = LeaveApplication
        fields = '__all__'
''',

    'apps/academic/serializers.py': '''"""Academic serializers"""
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
''',

    'apps/live_classes/serializers.py': '''"""Live Class serializers"""
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
''',

    'apps/students/serializers.py': '''"""Student serializers"""
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
''',

    'apps/guardians/serializers.py': '''"""Guardian serializers"""
from rest_framework import serializers
from .models import Guardian


class GuardianListSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    user_phone = serializers.CharField(source='user.phone', read_only=True)

    class Meta:
        model = Guardian
        fields = ['id', 'user_name', 'user_email', 'user_phone', 'occupation', 'photo']


class GuardianDetailSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Guardian
        fields = '__all__'

    def get_user(self, obj):
        return {
            'id': obj.user.id,
            'email': obj.user.email,
            'username': obj.user.username,
            'full_name': obj.user.get_full_name(),
            'phone': obj.user.phone,
        }
''',
}

print("\n📝 Creating Serializers...")
for filepath, content in SERIALIZERS_FILES.items():
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"  ✓ {filepath}")

print("\n✅ All serializers created!")

# Continue with views in next part...
print("\n" + "=" * 60)
print("Phase 1 Complete: Serializers Generated")
print("Run Phase 2 script to generate views...")
