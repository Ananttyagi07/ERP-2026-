"""Mail & SMS Communication models"""
from django.db import models
from apps.core.models import TimeStampedModel, CollegeIsolatedModel


class EmailLog(TimeStampedModel, CollegeIsolatedModel):
    """Bulk email sending logs"""
    RECEIVER_TYPES = [
        ('Student', 'Student'),
        ('Teacher', 'Teacher'),
        ('Employee', 'Employee'),
        ('Guardian', 'Guardian'),
    ]

    receiver_type = models.CharField(max_length=20, choices=RECEIVER_TYPES)
    receiver_ids = models.JSONField(default=list, help_text="List of recipient IDs")
    subject = models.CharField(max_length=255)
    body = models.TextField()
    attachment = models.FileField(upload_to='email_attachments/', null=True, blank=True)
    sent_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    send_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'email_logs'

    def __str__(self):
        return f"{self.receiver_type} - {self.subject}"


class SMSLog(TimeStampedModel, CollegeIsolatedModel):
    """Bulk SMS sending logs"""
    RECEIVER_TYPES = [
        ('Student', 'Student'),
        ('Teacher', 'Teacher'),
        ('Employee', 'Employee'),
        ('Guardian', 'Guardian'),
    ]

    session_year = models.CharField(max_length=20)
    receiver_type = models.CharField(max_length=20, choices=RECEIVER_TYPES)
    receiver_ids = models.JSONField(default=list)
    message = models.TextField()
    gateway = models.CharField(max_length=100)
    sent_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    send_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sms_logs'

    def __str__(self):
        return f"{self.receiver_type} - {self.send_date}"
