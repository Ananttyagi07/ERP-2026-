"""
Exam Management models
"""
from django.db import models
from apps.core.models import TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel


class Grade(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Grading system"""
    grade_name = models.CharField(max_length=10, help_text="e.g., A+, A, B+")
    point = models.DecimalField(max_digits=4, decimal_places=2)
    mark_from = models.DecimalField(max_digits=5, decimal_places=2)
    mark_to = models.DecimalField(max_digits=5, decimal_places=2)
    note = models.TextField(blank=True)

    class Meta:
        db_table = 'grades'
        ordering = ['-mark_from']

    def __str__(self):
        return f"{self.grade_name} ({self.mark_from}-{self.mark_to})"


class ExamTerm(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Exam terms (e.g., Midterm, Final)"""
    name = models.CharField(max_length=255)
    note = models.TextField(blank=True)

    class Meta:
        db_table = 'exam_terms'
        unique_together = [['college', 'name']]

    def __str__(self):
        return self.name


class ExamSchedule(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Exam schedule for subjects"""
    exam_term = models.ForeignKey(ExamTerm, on_delete=models.CASCADE, related_name='schedules')
    school_class = models.ForeignKey('academic.SchoolClass', on_delete=models.CASCADE)
    section = models.ForeignKey('academic.ClassSection', on_delete=models.CASCADE)
    subject = models.ForeignKey('academic.Subject', on_delete=models.CASCADE)
    exam_date = models.DateField()
    exam_time = models.TimeField()
    duration_minutes = models.IntegerField()
    room_no = models.CharField(max_length=50, blank=True)
    total_mark = models.DecimalField(max_digits=6, decimal_places=2)
    passing_mark = models.DecimalField(max_digits=6, decimal_places=2)
    note = models.TextField(blank=True)

    class Meta:
        db_table = 'exam_schedules'
        unique_together = [['exam_term', 'school_class', 'section', 'subject']]

    def __str__(self):
        return f"{self.exam_term.name} - {self.subject.name} - {self.exam_date}"


class ExamSuggestion(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Exam suggestions/study materials"""
    exam_term = models.ForeignKey(ExamTerm, on_delete=models.CASCADE)
    school_class = models.ForeignKey('academic.SchoolClass', on_delete=models.CASCADE)
    section = models.ForeignKey('academic.ClassSection', on_delete=models.CASCADE)
    subject = models.ForeignKey('academic.Subject', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    suggestion_file = models.FileField(upload_to='exam_suggestions/')

    class Meta:
        db_table = 'exam_suggestions'

    def __str__(self):
        return f"{self.title} - {self.subject.name}"


class ExamAttendanceRecord(TimeStampedModel, CollegeIsolatedModel):
    """Exam attendance tracking"""
    exam_schedule = models.ForeignKey(ExamSchedule, on_delete=models.CASCADE, related_name='attendances')
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])
    marked_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'exam_attendance_records'
        unique_together = [['exam_schedule', 'student']]

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.exam_schedule.subject.name} - {self.status}"
