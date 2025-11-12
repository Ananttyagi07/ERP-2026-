"""Miscellaneous models (Awards, Todo, FAQ)"""
from django.db import models
from apps.core.models import TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel


class Award(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Awards given to users"""
    USER_TYPES = [
        ('Student', 'Student'),
        ('Teacher', 'Teacher'),
        ('Employee', 'Employee'),
    ]

    academic_year = models.CharField(max_length=20)
    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    winner = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='awards')
    title = models.CharField(max_length=255)
    gift = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    note = models.TextField(blank=True)

    class Meta:
        db_table = 'awards'

    def __str__(self):
        return f"{self.title} - {self.winner.get_full_name()}"


class Todo(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Todo/task management"""
    USER_TYPES = [
        ('Teacher', 'Teacher'),
        ('Employee', 'Employee'),
        ('Admin', 'Admin'),
    ]
    WORK_STATUS = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    assign_to = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='assigned_todos')
    title = models.CharField(max_length=255)
    date = models.DateField()
    work_status = models.CharField(max_length=20, choices=WORK_STATUS, default='Pending')
    description = models.TextField(blank=True)
    comment = models.TextField(blank=True)

    class Meta:
        db_table = 'todos'

    def __str__(self):
        return self.title


class FAQ(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Frequently Asked Questions"""
    title = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        db_table = 'faqs'

    def __str__(self):
        return self.title
