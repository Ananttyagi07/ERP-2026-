"""
Marks and Results Management serializers
"""
from rest_framework import serializers
from .models import (
    ExamMark, MarkDistribution, ResultCard,
    MarkEmailLog, MarkSMSLog, ResultEmailLog, ResultSMSLog
)


class ExamMarkListSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    subject_name = serializers.CharField(source='exam_schedule.subject.name', read_only=True)
    grade_name = serializers.CharField(source='grade.grade_name', read_only=True)

    class Meta:
        model = ExamMark
        fields = [
            'id', 'student_name', 'subject_name', 'total_mark', 'grade_name', 'attendance_status'
        ]


class ExamMarkCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamMark
        fields = [
            'exam_schedule', 'student', 'written_mark', 'tutorial_mark',
            'practical_mark', 'viva_mark', 'attendance_status', 'note'
        ]


class ExamMarkDetailSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    subject_name = serializers.CharField(source='exam_schedule.subject.name', read_only=True)
    grade_name = serializers.CharField(source='grade.grade_name', read_only=True)
    exam_date = serializers.DateField(source='exam_schedule.exam_date', read_only=True)

    class Meta:
        model = ExamMark
        fields = '__all__'


class MarkDistributionListSerializer(serializers.ModelSerializer):
    exam_term_name = serializers.CharField(source='exam_term.name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)

    class Meta:
        model = MarkDistribution
        fields = [
            'id', 'exam_term_name', 'subject_name',
            'written_total', 'tutorial_total', 'practical_total', 'viva_total'
        ]


class MarkDistributionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarkDistribution
        fields = [
            'exam_term', 'school_class', 'subject',
            'written_total', 'tutorial_total', 'practical_total', 'viva_total'
        ]


class MarkDistributionDetailSerializer(serializers.ModelSerializer):
    exam_term_name = serializers.CharField(source='exam_term.name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    class_name = serializers.CharField(source='school_class.name', read_only=True)

    class Meta:
        model = MarkDistribution
        fields = '__all__'


class ResultCardListSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    exam_term_name = serializers.CharField(source='exam_term.name', read_only=True)
    overall_grade_name = serializers.CharField(source='overall_grade.grade_name', read_only=True)

    class Meta:
        model = ResultCard
        fields = [
            'id', 'student_name', 'exam_term_name', 'total_marks',
            'obtained_marks', 'percentage', 'overall_grade_name', 'result_status', 'merit_position'
        ]


class ResultCardDetailSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    exam_term_name = serializers.CharField(source='exam_term.name', read_only=True)
    class_name = serializers.CharField(source='school_class.name', read_only=True)
    overall_grade_name = serializers.CharField(source='overall_grade.grade_name', read_only=True)

    class Meta:
        model = ResultCard
        fields = '__all__'


class MarkEmailLogSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)

    class Meta:
        model = MarkEmailLog
        fields = '__all__'


class MarkSMSLogSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)

    class Meta:
        model = MarkSMSLog
        fields = '__all__'


class ResultEmailLogSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)

    class Meta:
        model = ResultEmailLog
        fields = '__all__'


class ResultSMSLogSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)

    class Meta:
        model = ResultSMSLog
        fields = '__all__'
