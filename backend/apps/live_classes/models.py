"""
Live Class and Assignment models
"""
from django.db import models
from apps.core.models import TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel


class LiveClassType(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Type of live class (Zoom, Google Meet, etc.)"""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'live_class_types'

    def __str__(self):
        return self.name


class LiveClass(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Live class scheduling"""
    school_class = models.ForeignKey('academic.SchoolClass', on_delete=models.CASCADE, related_name='live_classes')
    section = models.ForeignKey('academic.ClassSection', on_delete=models.CASCADE, related_name='live_classes')
    subject = models.ForeignKey('academic.Subject', on_delete=models.CASCADE, related_name='live_classes')
    teacher = models.ForeignKey('teachers.Teacher', on_delete=models.CASCADE, related_name='live_classes')
    live_class_type = models.ForeignKey(LiveClassType, on_delete=models.PROTECT, related_name='classes')

    class_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    meeting_url = models.URLField(blank=True)
    note = models.TextField(blank=True)
    send_notification = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=[('Scheduled', 'Scheduled'), ('Ongoing', 'Ongoing'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='Scheduled')

    class Meta:
        db_table = 'live_classes'

    def __str__(self):
        return f"{self.subject.name} - {self.class_date} {self.start_time}"


class Assignment(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Assignment management"""
    title = models.CharField(max_length=255)
    school_class = models.ForeignKey('academic.SchoolClass', on_delete=models.CASCADE, related_name='assignments')
    section = models.ForeignKey('academic.ClassSection', on_delete=models.CASCADE, related_name='assignments')
    subject = models.ForeignKey('academic.Subject', on_delete=models.CASCADE, related_name='assignments')

    assignment_date = models.DateField()
    submission_date = models.DateField()
    attachment = models.FileField(upload_to='assignments/', null=True, blank=True)
    note = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=[('Active', 'Active'), ('Closed', 'Closed')], default='Active')

    class Meta:
        db_table = 'assignments'

    def __str__(self):
        return self.title
