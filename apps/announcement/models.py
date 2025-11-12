"""Announcement models (Notice, News, Holiday)"""
from django.db import models
from apps.core.models import TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel


class Notice(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Notices/Announcements"""
    NOTICE_FOR_CHOICES = [
        ('All', 'All'),
        ('Student', 'Student'),
        ('Teacher', 'Teacher'),
        ('Employee', 'Employee'),
        ('Guardian', 'Guardian'),
    ]

    title = models.CharField(max_length=255)
    date = models.DateField()
    notice_for = models.CharField(max_length=20, choices=NOTICE_FOR_CHOICES)
    notice_text = models.TextField()
    is_view_on_web = models.BooleanField(default=False)

    class Meta:
        db_table = 'notices'

    def __str__(self):
        return self.title


class News(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """News items"""
    title = models.CharField(max_length=255)
    date = models.DateField()
    image = models.ImageField(upload_to='news/', null=True, blank=True)
    news_text = models.TextField()
    is_view_on_web = models.BooleanField(default=False)

    class Meta:
        db_table = 'news'
        verbose_name_plural = 'news'

    def __str__(self):
        return self.title


class Holiday(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Holiday calendar"""
    title = models.CharField(max_length=255)
    from_date = models.DateField()
    to_date = models.DateField()
    note = models.TextField()
    is_view_on_web = models.BooleanField(default=False)

    class Meta:
        db_table = 'holidays'

    def __str__(self):
        return self.title
