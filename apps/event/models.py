"""Event Management models"""
from django.db import models
from apps.core.models import TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel


class Event(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """School events"""
    EVENT_FOR_CHOICES = [
        ('All', 'All'),
        ('Student', 'Student'),
        ('Teacher', 'Teacher'),
        ('Employee', 'Employee'),
    ]

    title = models.CharField(max_length=255)
    event_for = models.CharField(max_length=20, choices=EVENT_FOR_CHOICES)
    event_place = models.CharField(max_length=255)
    from_date = models.DateField()
    to_date = models.DateField()
    image = models.ImageField(upload_to='events/', null=True, blank=True)
    note = models.TextField(blank=True)
    is_view_on_web = models.BooleanField(default=False)

    class Meta:
        db_table = 'events'

    def __str__(self):
        return self.title
