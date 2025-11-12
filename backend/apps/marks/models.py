"""
Marks and Results Management models
"""
from django.db import models
from apps.core.models import TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel


class ExamMark(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Student exam marks"""
    exam_schedule = models.ForeignKey('exam_management.ExamSchedule', on_delete=models.CASCADE, related_name='marks')
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    written_mark = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    tutorial_mark = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    practical_mark = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    viva_mark = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    total_mark = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    grade = models.ForeignKey('exam_management.Grade', on_delete=models.SET_NULL, null=True, blank=True)
    attendance_status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')], default='Present')
    note = models.TextField(blank=True)

    class Meta:
        db_table = 'exam_marks'
        unique_together = [['exam_schedule', 'student']]

    def save(self, *args, **kwargs):
        self.total_mark = self.written_mark + self.tutorial_mark + self.practical_mark + self.viva_mark
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.exam_schedule.subject.name} - {self.total_mark}"


class MarkDistribution(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Mark distribution configuration"""
    exam_term = models.ForeignKey('exam_management.ExamTerm', on_delete=models.CASCADE)
    school_class = models.ForeignKey('academic.SchoolClass', on_delete=models.CASCADE)
    subject = models.ForeignKey('academic.Subject', on_delete=models.CASCADE)
    written_total = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    tutorial_total = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    practical_total = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    viva_total = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    class Meta:
        db_table = 'mark_distributions'
        unique_together = [['exam_term', 'school_class', 'subject']]

    def __str__(self):
        return f"{self.exam_term.name} - {self.subject.name}"


class ResultCard(TimeStampedModel, CollegeIsolatedModel):
    """Generated result cards"""
    exam_term = models.ForeignKey('exam_management.ExamTerm', on_delete=models.CASCADE)
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    school_class = models.ForeignKey('academic.SchoolClass', on_delete=models.CASCADE)
    section = models.ForeignKey('academic.ClassSection', on_delete=models.CASCADE)
    total_marks = models.DecimalField(max_digits=7, decimal_places=2)
    obtained_marks = models.DecimalField(max_digits=7, decimal_places=2)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    overall_grade = models.ForeignKey('exam_management.Grade', on_delete=models.SET_NULL, null=True)
    result_status = models.CharField(max_length=10, choices=[('Pass', 'Pass'), ('Fail', 'Fail')])
    merit_position = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'result_cards'
        unique_together = [['exam_term', 'student']]

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.exam_term.name} - {self.percentage}%"


class MarkEmailLog(TimeStampedModel, CollegeIsolatedModel):
    """Log of mark notification emails"""
    exam_schedule = models.ForeignKey('exam_management.ExamSchedule', on_delete=models.CASCADE)
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    receiver_email = models.EmailField()
    subject = models.CharField(max_length=255)
    body = models.TextField()
    template = models.ForeignKey('templates.EmailTemplate', on_delete=models.SET_NULL, null=True, blank=True)
    sent_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'mark_email_logs'

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.receiver_email}"


class MarkSMSLog(TimeStampedModel, CollegeIsolatedModel):
    """Log of mark notification SMS"""
    exam_schedule = models.ForeignKey('exam_management.ExamSchedule', on_delete=models.CASCADE)
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    receiver_phone = models.CharField(max_length=20)
    message = models.TextField()
    template = models.ForeignKey('templates.SMSTemplate', on_delete=models.SET_NULL, null=True, blank=True)
    gateway = models.CharField(max_length=100)
    sent_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'mark_sms_logs'

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.receiver_phone}"


class ResultEmailLog(TimeStampedModel, CollegeIsolatedModel):
    """Log of result notification emails"""
    exam_term = models.ForeignKey('exam_management.ExamTerm', on_delete=models.CASCADE)
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    receiver_email = models.EmailField()
    subject = models.CharField(max_length=255)
    body = models.TextField()
    template = models.ForeignKey('templates.EmailTemplate', on_delete=models.SET_NULL, null=True, blank=True)
    sent_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'result_email_logs'

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.receiver_email}"


class ResultSMSLog(TimeStampedModel, CollegeIsolatedModel):
    """Log of result notification SMS"""
    exam_term = models.ForeignKey('exam_management.ExamTerm', on_delete=models.CASCADE)
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    receiver_phone = models.CharField(max_length=20)
    message = models.TextField()
    template = models.ForeignKey('templates.SMSTemplate', on_delete=models.SET_NULL, null=True, blank=True)
    gateway = models.CharField(max_length=100)
    sent_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'result_sms_logs'

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.receiver_phone}"
