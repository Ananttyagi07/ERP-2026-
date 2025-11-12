"""
Guardian management models
"""
from django.db import models
from apps.core.models import TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel


class Guardian(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Guardian/Parent profile"""
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='guardian_profile')

    # Basic Info
    national_id = models.CharField(max_length=50, blank=True)
    occupation = models.CharField(max_length=255, blank=True)
    designation = models.CharField(max_length=255, blank=True)
    income = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    blood_group = models.CharField(max_length=5, choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')], blank=True)
    religion = models.CharField(max_length=50, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    # Address
    present_address = models.TextField(blank=True)
    permanent_address = models.TextField(blank=True)

    # Additional Info
    photo = models.ImageField(upload_to='guardians/photos/', null=True, blank=True)
    other_info = models.TextField(blank=True)

    class Meta:
        db_table = 'guardians'

    def __str__(self):
        return f"Guardian: {self.user.get_full_name()}"
