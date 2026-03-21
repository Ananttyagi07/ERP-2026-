#!/usr/bin/env python3
"""Generate remaining Superadmin models - Part 2"""

MODELS = {
    # Messaging
    'apps/messaging/models.py': '''"""Internal Messaging System models"""
from django.db import models
from apps.core.models import TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel


class Message(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Internal messages between users"""
    sender = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=255)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    is_draft = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'messages'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.sender.get_full_name()} to {self.receiver.get_full_name()}: {self.subject}"
''',

    # Communication (Mail & SMS)
    'apps/communication/models.py': '''"""Mail & SMS Communication models"""
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
''',

    # Complain
    'apps/complain/models.py': '''"""Complaint Management models"""
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
''',

    # Announcement
    'apps/announcement/models.py': '''"""Announcement models (Notice, News, Holiday)"""
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
''',

    # Scholarship
    'apps/scholarship/models.py': '''"""Scholarship Management models"""
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
''',

    # Event
    'apps/event/models.py': '''"""Event Management models"""
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
''',
}

print("🚀 Generating remaining models (Part 2)...")
print("=" * 70)

for filepath, content in MODELS.items():
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"✓ {filepath}")

print("\n✅ Part 2 Complete!")
print("Models created: Messaging, Communication, Complain, Announcement, Scholarship, Event")
