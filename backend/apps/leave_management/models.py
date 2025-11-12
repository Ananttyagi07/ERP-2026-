"""
Leave Management models
"""
from django.db import models
from apps.core.models import TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel


class LeaveType(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Leave type definition"""
    name = models.CharField(max_length=255)
    applicant_type = models.CharField(max_length=50, choices=[('Employee', 'Employee'), ('Teacher', 'Teacher'), ('Student', 'Student')])
    days_allowed = models.IntegerField(default=0, help_text="Number of days allowed per year")
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'leave_types'

    def __str__(self):
        return f"{self.name} ({self.applicant_type})"


class LeaveApplication(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Leave application with approval workflow"""
    leave_type = models.ForeignKey(LeaveType, on_delete=models.PROTECT, related_name='applications')
    applicant = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='leave_applications')
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    attachment = models.FileField(upload_to='leave_applications/', null=True, blank=True)

    # Approval workflow
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Declined', 'Declined')],
        default='Pending'
    )
    approved_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='leave_approvals')
    approval_date = models.DateTimeField(null=True, blank=True)
    approval_note = models.TextField(blank=True)

    class Meta:
        db_table = 'leave_applications'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.applicant.get_full_name()} - {self.leave_type.name} ({self.status})"

    @property
    def total_days(self):
        return (self.end_date - self.start_date).days + 1
