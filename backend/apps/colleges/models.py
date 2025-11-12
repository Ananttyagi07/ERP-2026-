"""
College models for multi-college support within a university
"""
from django.db import models
from apps.core.models import TimeStampedModel, SoftDeleteModel


class College(TimeStampedModel, SoftDeleteModel):
    """
    Model representing a college/branch within the university
    Each university can have multiple colleges
    """
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True, db_index=True)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    established_date = models.DateField(null=True, blank=True)

    # Principal/Head of College (will be set after User model is created)
    principal = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='college_principal_of'
    )

    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        db_table = 'colleges'
        ordering = ['name']
        verbose_name = 'College'
        verbose_name_plural = 'Colleges'

    def __str__(self):
        return f"{self.name} ({self.code})"


class Department(TimeStampedModel, SoftDeleteModel):
    """
    Academic department within a college
    """
    college = models.ForeignKey(
        College,
        on_delete=models.CASCADE,
        related_name='departments'
    )
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    # Head of Department
    head = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='department_head_of'
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'departments'
        ordering = ['college', 'name']
        unique_together = [['college', 'code']]
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'
        indexes = [
            models.Index(fields=['college', 'code']),
        ]

    def __str__(self):
        return f"{self.college.code} - {self.name}"
