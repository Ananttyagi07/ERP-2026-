"""
Template management models (SMS & Email)
"""
from django.db import models
from apps.core.models import TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel


class SMSTemplate(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """SMS Template with dynamic tags"""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    message_body = models.TextField(help_text="Use tags: {name}, {email}, {phone}, {school}, {class}, {section}, {roll}, {subject}")
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'sms_templates'

    def __str__(self):
        return self.name


class EmailTemplate(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Email Template with dynamic tags"""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    subject = models.CharField(max_length=255)
    message_body = models.TextField(help_text="Use tags: {name}, {email}, {phone}, {school}, {class}, {section}, {roll}, {subject}")
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'email_templates'

    def __str__(self):
        return self.name
