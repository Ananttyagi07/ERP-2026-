"""
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
