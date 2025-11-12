"""
Certificate Generation models
"""
from django.db import models
from apps.core.models import TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel


class CertificateType(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Certificate templates"""
    certificate_name = models.CharField(max_length=255)
    school_name = models.CharField(max_length=255)
    certificate_text = models.TextField(help_text="Use tags: [name], [class], [roll], [session], [date], [father_name], [mother_name]")
    footer_left_text = models.CharField(max_length=255, blank=True)
    footer_middle_text = models.CharField(max_length=255, blank=True)
    footer_right_text = models.CharField(max_length=255, blank=True)
    background = models.ImageField(upload_to='certificate_backgrounds/', null=True, blank=True)

    class Meta:
        db_table = 'certificate_types'

    def __str__(self):
        return self.certificate_name


class CertificateGeneration(TimeStampedModel, CollegeIsolatedModel):
    """Generated certificates"""
    certificate_type = models.ForeignKey(CertificateType, on_delete=models.CASCADE)
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    school_class = models.ForeignKey('academic.SchoolClass', on_delete=models.CASCADE)
    section = models.ForeignKey('academic.ClassSection', on_delete=models.CASCADE)
    generated_certificate = models.FileField(upload_to='generated_certificates/', null=True, blank=True)
    generated_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'certificate_generations'

    def __str__(self):
        return f"{self.certificate_type.certificate_name} - {self.student.user.get_full_name()}"
