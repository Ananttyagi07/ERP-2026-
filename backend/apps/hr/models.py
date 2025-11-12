"""
Human Resource models (Designation, Employee)
"""
from django.db import models
from apps.core.models import TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel


class Designation(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Job designation/position"""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'designations'

    def __str__(self):
        return self.name


class Employee(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Employee profile (3-tab form: Basic, Academic, Other Info)"""
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='employee_profile')

    # Basic Info
    designation = models.ForeignKey(Designation, on_delete=models.PROTECT, related_name='employees')
    national_id = models.CharField(max_length=50, blank=True)
    blood_group = models.CharField(max_length=5, choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')], blank=True)
    religion = models.CharField(max_length=50, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    joining_date = models.DateField()
    present_address = models.TextField(blank=True)
    permanent_address = models.TextField(blank=True)

    # Academic Info
    qualification = models.CharField(max_length=255, blank=True)
    experience_years = models.IntegerField(default=0)

    # Other Info
    facebook = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    pinterest = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    resume = models.FileField(upload_to='employees/resumes/', null=True, blank=True)
    photo = models.ImageField(upload_to='employees/photos/', null=True, blank=True)
    other_info = models.TextField(blank=True)

    class Meta:
        db_table = 'employees'

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.designation.name}"
