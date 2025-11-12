"""
Front Office models (Visitor, Call Log, Postal)
"""
from django.db import models
from apps.core.models import TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel


class VisitorPurpose(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Purpose of visit"""
    purpose = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'visitor_purposes'

    def __str__(self):
        return self.purpose


class VisitorInfo(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Visitor check-in/out tracking"""
    purpose = models.ForeignKey(VisitorPurpose, on_delete=models.PROTECT, related_name='visitors')
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    visitor_id = models.CharField(max_length=50, blank=True, help_text="National ID, Passport, etc.")
    meet_staff_id = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, related_name='visitors_met')
    meet_user_type = models.CharField(max_length=50, choices=[('Staff', 'Staff'), ('Student', 'Student'), ('Faculty', 'Faculty')])
    number_of_people = models.IntegerField(default=1)
    check_in_date = models.DateField()
    check_in_time = models.TimeField()
    check_out_date = models.DateField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    note = models.TextField(blank=True)
    photo = models.ImageField(upload_to='visitors/photos/', null=True, blank=True)
    attachment = models.FileField(upload_to='visitors/attachments/', null=True, blank=True)

    class Meta:
        db_table = 'visitor_info'

    def __str__(self):
        return f"{self.name} - {self.check_in_date}"


class CallLog(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Call log tracking"""
    call_type = models.CharField(max_length=20, choices=[('Incoming', 'Incoming'), ('Outgoing', 'Outgoing')])
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    call_date = models.DateField()
    follow_up_date = models.DateField(null=True, blank=True)
    call_duration = models.CharField(max_length=50, blank=True)
    note = models.TextField(blank=True)
    call_purpose = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'call_logs'

    def __str__(self):
        return f"{self.call_type} - {self.name}"


class PostalDispatch(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Postal dispatch tracking"""
    to_title = models.CharField(max_length=255)
    reference_number = models.CharField(max_length=100, unique=True)
    address = models.TextField()
    note = models.TextField(blank=True)
    dispatch_date = models.DateField()
    attachment = models.FileField(upload_to='postal/dispatch/', null=True, blank=True)

    class Meta:
        db_table = 'postal_dispatches'

    def __str__(self):
        return f"Dispatch: {self.reference_number}"


class PostalReceive(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Postal receive tracking"""
    from_title = models.CharField(max_length=255)
    reference_number = models.CharField(max_length=100, unique=True)
    address = models.TextField()
    note = models.TextField(blank=True)
    receive_date = models.DateField()
    receiver_type = models.CharField(max_length=50, choices=[('Admin', 'Admin'), ('Guardian', 'Guardian'), ('Student', 'Student'), ('Teacher', 'Teacher'), ('Staff', 'Staff')])
    attachment = models.FileField(upload_to='postal/receive/', null=True, blank=True)

    class Meta:
        db_table = 'postal_receives'

    def __str__(self):
        return f"Receive: {self.reference_number}"
