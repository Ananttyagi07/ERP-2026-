"""
Online Exam models
"""
from django.db import models
from apps.core.models import TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel


class ExamInstruction(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Reusable exam instructions"""
    title = models.CharField(max_length=255)
    instruction = models.TextField()

    class Meta:
        db_table = 'exam_instructions'

    def __str__(self):
        return self.title


class QuestionBank(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Question bank for online exams"""
    QUESTION_TYPES = [
        ('Multiple Choice', 'Multiple Choice'),
        ('True/False', 'True/False'),
        ('Short Answer', 'Short Answer'),
    ]
    QUESTION_LEVELS = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]

    school_class = models.ForeignKey('academic.SchoolClass', on_delete=models.CASCADE)
    section = models.ForeignKey('academic.ClassSection', on_delete=models.CASCADE)
    subject = models.ForeignKey('academic.Subject', on_delete=models.CASCADE)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    question_level = models.CharField(max_length=10, choices=QUESTION_LEVELS)
    question = models.TextField()
    option_a = models.CharField(max_length=500, blank=True)
    option_b = models.CharField(max_length=500, blank=True)
    option_c = models.CharField(max_length=500, blank=True)
    option_d = models.CharField(max_length=500, blank=True)
    correct_answer = models.CharField(max_length=500)
    mark = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        db_table = 'question_bank'

    def __str__(self):
        return f"{self.subject.name} - {self.question_type}"


class OnlineExam(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Online exam configuration"""
    exam_title = models.CharField(max_length=255)
    school_class = models.ForeignKey('academic.SchoolClass', on_delete=models.CASCADE)
    section = models.ForeignKey('academic.ClassSection', on_delete=models.CASCADE)
    subject = models.ForeignKey('academic.Subject', on_delete=models.CASCADE)
    instruction = models.ForeignKey(ExamInstruction, on_delete=models.SET_NULL, null=True, blank=True)
    exam_date = models.DateField()
    exam_time = models.TimeField()
    duration_minutes = models.IntegerField(help_text="Duration in minutes")
    total_mark = models.DecimalField(max_digits=6, decimal_places=2)
    passing_mark = models.DecimalField(max_digits=6, decimal_places=2)
    publish_status = models.BooleanField(default=False)
    questions = models.ManyToManyField(QuestionBank, related_name='exams')

    class Meta:
        db_table = 'online_exams'

    def __str__(self):
        return f"{self.exam_title} - {self.exam_date}"


class OnlineExamResult(TimeStampedModel, CollegeIsolatedModel):
    """Online exam results"""
    exam = models.ForeignKey(OnlineExam, on_delete=models.CASCADE, related_name='results')
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    answers = models.JSONField(default=dict, help_text="Student answers")
    obtained_mark = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(max_length=10, choices=[('Pass', 'Pass'), ('Fail', 'Fail')])
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'online_exam_results'
        unique_together = [['exam', 'student']]

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.exam.exam_title} - {self.obtained_mark}"
