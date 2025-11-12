"""
Student management models
"""
from django.db import models
from apps.core.models import TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel


class Student(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Student profile"""
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='student_profile')

    # Academic Info
    school_class = models.ForeignKey('academic.SchoolClass', on_delete=models.PROTECT, related_name='students')
    section = models.ForeignKey('academic.ClassSection', on_delete=models.PROTECT, related_name='students')
    roll_number = models.CharField(max_length=50)
    registration_number = models.CharField(max_length=100, unique=True)
    admission_date = models.DateField()

    # Basic Info
    national_id = models.CharField(max_length=50, blank=True)
    blood_group = models.CharField(max_length=5, choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')], blank=True)
    religion = models.CharField(max_length=50, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    present_address = models.TextField(blank=True)
    permanent_address = models.TextField(blank=True)

    # Additional Info
    photo = models.ImageField(upload_to='students/photos/', null=True, blank=True)
    other_info = models.TextField(blank=True)

    class Meta:
        db_table = 'students'
        unique_together = [['college', 'roll_number', 'school_class', 'section']]

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.roll_number}"


class StudentParent(TimeStampedModel, SoftDeleteModel):
    """Relationship between student and guardian"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='parents')
    guardian = models.ForeignKey('guardians.Guardian', on_delete=models.CASCADE, related_name='children')
    relationship = models.CharField(max_length=50, choices=[('Father', 'Father'), ('Mother', 'Mother'), ('Guardian', 'Guardian'), ('Other', 'Other')])
    is_primary = models.BooleanField(default=False, help_text="Primary contact")

    class Meta:
        db_table = 'student_parents'
        unique_together = [['student', 'guardian']]

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.guardian.user.get_full_name()} ({self.relationship})"
