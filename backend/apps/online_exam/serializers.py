"""
Online Exam serializers
"""
from rest_framework import serializers
from .models import ExamInstruction, QuestionBank, OnlineExam, OnlineExamResult


class ExamInstructionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamInstruction
        fields = ['id', 'title', 'created_at']


class ExamInstructionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamInstruction
        fields = ['title', 'instruction']


class ExamInstructionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamInstruction
        fields = '__all__'


class QuestionBankListSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    class_name = serializers.CharField(source='school_class.name', read_only=True)

    class Meta:
        model = QuestionBank
        fields = ['id', 'subject_name', 'class_name', 'question_type', 'question_level', 'mark']


class QuestionBankCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionBank
        fields = [
            'school_class', 'section', 'subject', 'question_type', 'question_level',
            'question', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer', 'mark'
        ]


class QuestionBankDetailSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    class_name = serializers.CharField(source='school_class.name', read_only=True)
    section_name = serializers.CharField(source='section.name', read_only=True)

    class Meta:
        model = QuestionBank
        fields = '__all__'


class OnlineExamListSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    class_name = serializers.CharField(source='school_class.name', read_only=True)
    question_count = serializers.SerializerMethodField()

    class Meta:
        model = OnlineExam
        fields = ['id', 'exam_title', 'subject_name', 'class_name', 'exam_date', 'publish_status', 'question_count']

    def get_question_count(self, obj):
        return obj.questions.count()


class OnlineExamCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnlineExam
        fields = [
            'exam_title', 'school_class', 'section', 'subject', 'instruction',
            'exam_date', 'exam_time', 'duration_minutes', 'total_mark', 'passing_mark', 'questions'
        ]


class OnlineExamDetailSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    class_name = serializers.CharField(source='school_class.name', read_only=True)
    section_name = serializers.CharField(source='section.name', read_only=True)
    instruction_text = serializers.CharField(source='instruction.instruction', read_only=True)
    questions_detail = QuestionBankDetailSerializer(source='questions', many=True, read_only=True)

    class Meta:
        model = OnlineExam
        fields = '__all__'


class OnlineExamResultListSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    exam_title = serializers.CharField(source='exam.exam_title', read_only=True)

    class Meta:
        model = OnlineExamResult
        fields = ['id', 'student_name', 'exam_title', 'obtained_mark', 'status', 'submitted_at']


class OnlineExamResultCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnlineExamResult
        fields = ['exam', 'student', 'answers', 'obtained_mark', 'status']


class OnlineExamResultDetailSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    exam_detail = OnlineExamDetailSerializer(source='exam', read_only=True)

    class Meta:
        model = OnlineExamResult
        fields = '__all__'
