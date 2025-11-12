"""
Superadmin management models
"""
from django.db import models
from apps.core.models import TimeStampedModel, SoftDeleteModel


class SuperAdminProfile(TimeStampedModel, SoftDeleteModel):
    """Extended profile for Superadmin users"""
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='superadmin_profile')
    national_id = models.CharField(max_length=50, blank=True)
    blood_group = models.CharField(max_length=5, choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')], blank=True)
    religion = models.CharField(max_length=50, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    present_address = models.TextField(blank=True)
    permanent_address = models.TextField(blank=True)
    resume = models.FileField(upload_to='superadmin/resumes/', null=True, blank=True)
    photo = models.ImageField(upload_to='superadmin/photos/', null=True, blank=True)
    other_info = models.TextField(blank=True)

    class Meta:
        db_table = 'superadmin_profiles'

    def __str__(self):
        return f"SuperAdmin - {self.user.get_full_name()}"
