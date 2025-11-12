"""
Exam Management serializers
"""
from rest_framework import serializers
from .models import Grade, ExamTerm, ExamSchedule, ExamSuggestion, ExamAttendanceRecord


class GradeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ['id', 'grade_name', 'point', 'mark_from', 'mark_to']


class GradeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ['grade_name', 'point', 'mark_from', 'mark_to', 'note']


class GradeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'


class ExamTermListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamTerm
        fields = ['id', 'name', 'created_at']


class ExamTermCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamTerm
        fields = ['name', 'note']


class ExamTermDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamTerm
        fields = '__all__'


class ExamScheduleListSerializer(serializers.ModelSerializer):
    exam_term_name = serializers.CharField(source='exam_term.name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    class_name = serializers.CharField(source='school_class.name', read_only=True)

    class Meta:
        model = ExamSchedule
        fields = [
            'id', 'exam_term_name', 'subject_name', 'class_name',
            'exam_date', 'exam_time', 'total_mark'
        ]


class ExamScheduleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamSchedule
        fields = [
            'exam_term', 'school_class', 'section', 'subject',
            'exam_date', 'exam_time', 'duration_minutes', 'room_no',
            'total_mark', 'passing_mark', 'note'
        ]


class ExamScheduleDetailSerializer(serializers.ModelSerializer):
    exam_term_name = serializers.CharField(source='exam_term.name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    class_name = serializers.CharField(source='school_class.name', read_only=True)
    section_name = serializers.CharField(source='section.name', read_only=True)

    class Meta:
        model = ExamSchedule
        fields = '__all__'


class ExamSuggestionListSerializer(serializers.ModelSerializer):
    exam_term_name = serializers.CharField(source='exam_term.name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)

    class Meta:
        model = ExamSuggestion
        fields = ['id', 'title', 'exam_term_name', 'subject_name', 'created_at']


class ExamSuggestionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamSuggestion
        fields = ['exam_term', 'school_class', 'section', 'subject', 'title', 'suggestion_file']


class ExamSuggestionDetailSerializer(serializers.ModelSerializer):
    exam_term_name = serializers.CharField(source='exam_term.name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    class_name = serializers.CharField(source='school_class.name', read_only=True)

    class Meta:
        model = ExamSuggestion
        fields = '__all__'


class ExamAttendanceRecordListSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    subject_name = serializers.CharField(source='exam_schedule.subject.name', read_only=True)

    class Meta:
        model = ExamAttendanceRecord
        fields = ['id', 'student_name', 'subject_name', 'status']


class ExamAttendanceRecordCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamAttendanceRecord
        fields = ['exam_schedule', 'student', 'status']


class ExamAttendanceRecordDetailSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    exam_schedule_detail = ExamScheduleDetailSerializer(source='exam_schedule', read_only=True)

    class Meta:
        model = ExamAttendanceRecord
        fields = '__all__'
