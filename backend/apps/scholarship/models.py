"""Scholarship Management models"""
from django.db import models
from apps.core.models import TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel


class ScholarshipCandidate(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Scholarship candidates"""
    academic_year = models.CharField(max_length=20)
    school_class = models.ForeignKey('academic.SchoolClass', on_delete=models.CASCADE)
    section = models.ForeignKey('academic.ClassSection', on_delete=models.CASCADE)
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='scholarship_applications')
    note = models.TextField(blank=True)

    class Meta:
        db_table = 'scholarship_candidates'

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.academic_year}"


class Donor(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Scholarship donors"""
    DONOR_TYPES = [
        ('Individual', 'Individual'),
        ('Organization', 'Organization'),
        ('Corporate', 'Corporate'),
    ]

    academic_year = models.CharField(max_length=20)
    donor_type = models.CharField(max_length=20, choices=DONOR_TYPES)
    donor_name = models.CharField(max_length=255)
    contact_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    address = models.TextField(blank=True)
    note = models.TextField(blank=True)

    class Meta:
        db_table = 'donors'

    def __str__(self):
        return self.donor_name


class Scholarship(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Scholarship awards"""
    candidate = models.ForeignKey(ScholarshipCandidate, on_delete=models.CASCADE, related_name='scholarships')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    note = models.TextField(blank=True)

    class Meta:
        db_table = 'scholarships'

    def __str__(self):
        return f"{self.candidate.student.user.get_full_name()} - ₹{self.amount}"
