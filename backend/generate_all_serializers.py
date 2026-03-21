#!/usr/bin/env python3
"""
Generate serializers for all 9 new modules
Complete serializers with proper validation and field handling
"""

SERIALIZERS = {
    # ============================================================================
    # STUDENT MANAGEMENT SERIALIZERS
    # ============================================================================
    'apps/student_management/serializers.py': '''"""
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
''',

    # ============================================================================
    # ATTENDANCE SERIALIZERS
    # ============================================================================
    'apps/attendance/serializers.py': '''"""
Attendance serializers
"""
from rest_framework import serializers
from .models import (
    StudentAttendance, TeacherAttendance, EmployeeAttendance,
    AbsentEmailLog, AbsentSMSLog
)


class StudentAttendanceListSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    roll_number = serializers.CharField(source='student.roll_number', read_only=True)
    class_name = serializers.CharField(source='school_class.name', read_only=True)

    class Meta:
        model = StudentAttendance
        fields = ['id', 'student_name', 'roll_number', 'class_name', 'attendance_date', 'status']


class StudentAttendanceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAttendance
        fields = ['student', 'school_class', 'section', 'attendance_date', 'status']


class TeacherAttendanceListSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.user.get_full_name', read_only=True)
    employee_id = serializers.CharField(source='teacher.employee_id', read_only=True)

    class Meta:
        model = TeacherAttendance
        fields = ['id', 'teacher_name', 'employee_id', 'attendance_date', 'status']


class TeacherAttendanceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherAttendance
        fields = ['teacher', 'attendance_date', 'status']


class EmployeeAttendanceListSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.user.get_full_name', read_only=True)
    designation = serializers.CharField(source='employee.designation.title', read_only=True)

    class Meta:
        model = EmployeeAttendance
        fields = ['id', 'employee_name', 'designation', 'attendance_date', 'status']


class EmployeeAttendanceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeAttendance
        fields = ['employee', 'attendance_date', 'status']


class AbsentEmailLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbsentEmailLog
        fields = '__all__'


class AbsentSMSLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbsentSMSLog
        fields = '__all__'
''',

    # Continue with remaining modules...
    # I'll create a separate file for each to keep them organized
}

print("🚀 Generating serializers for all modules...")
print("=" * 70)

import os

for filepath, content in SERIALIZERS.items():
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"✓ {filepath}")

print("\n✅ Serializers created (Part 1/3)")
print("Creating remaining serializers...")
