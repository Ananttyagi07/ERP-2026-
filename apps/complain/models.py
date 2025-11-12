"""Complaint Management models"""
from django.db import models
from apps.core.models import TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel


class ComplainType(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Complaint categories"""
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'complain_types'
        unique_together = [['college', 'name']]

    def __str__(self):
        return self.name


class Complain(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Complaint records"""
    USER_TYPES = [
        ('Student', 'Student'),
        ('Teacher', 'Teacher'),
        ('Employee', 'Employee'),
        ('Guardian', 'Guardian'),
    ]

    academic_year = models.CharField(max_length=20)
    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    complain_by = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='complains_made')
    complain_type = models.ForeignKey(ComplainType, on_delete=models.CASCADE)
    complain_date = models.DateField()
    complain_text = models.TextField()
    action_taken = models.TextField(blank=True)
    action_date = models.DateField(null=True, blank=True)
    action_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='complains_actioned')

    class Meta:
        db_table = 'complains'

    def __str__(self):
        return f"{self.complain_by.get_full_name()} - {self.complain_type.name}"
