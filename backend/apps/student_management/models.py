"""
Student Management models (enhanced student features)
"""
from django.db import models
from apps.core.models import TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel


class StudentType(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Student type (Undergraduate, Postgraduate, etc.)"""
    name = models.CharField(max_length=255, help_text="e.g., Undergraduate, Postgraduate")
    note = models.TextField(blank=True)

    class Meta:
        db_table = 'student_types'
        unique_together = [['college', 'name']]

    def __str__(self):
        return self.name


class OnlineAdmission(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Online admission applications"""
    student_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    school_class = models.ForeignKey('academic.SchoolClass', on_delete=models.CASCADE, related_name='online_admissions')
    photo = models.ImageField(upload_to='online_admissions/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending')
    application_data = models.JSONField(default=dict, help_text="Full application form data")

    class Meta:
        db_table = 'online_admissions'

    def __str__(self):
        return f"{self.student_name} - {self.status}"


class StudentActivity(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Student activities tracking"""
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='activities')
    school_class = models.ForeignKey('academic.SchoolClass', on_delete=models.CASCADE)
    section = models.ForeignKey('academic.ClassSection', on_delete=models.CASCADE)
    activity = models.TextField()
    activity_date = models.DateField()

    class Meta:
        db_table = 'student_activities'

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.activity_date}"
