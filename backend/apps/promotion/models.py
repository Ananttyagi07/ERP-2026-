"""
Student Promotion models
"""
from django.db import models
from apps.core.models import TimeStampedModel, CollegeIsolatedModel


class StudentPromotion(TimeStampedModel, CollegeIsolatedModel):
    """Student class promotion records"""
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='promotions')
    from_class = models.ForeignKey('academic.SchoolClass', on_delete=models.CASCADE, related_name='promoted_from')
    from_section = models.ForeignKey('academic.ClassSection', on_delete=models.CASCADE, related_name='promoted_from_section')
    to_class = models.ForeignKey('academic.SchoolClass', on_delete=models.CASCADE, related_name='promoted_to')
    to_section = models.ForeignKey('academic.ClassSection', on_delete=models.CASCADE, related_name='promoted_to_section')
    session_from = models.CharField(max_length=20, help_text="e.g., 2024")
    session_to = models.CharField(max_length=20, help_text="e.g., 2025")
    promoted_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    promotion_date = models.DateField(auto_now_add=True)
    note = models.TextField(blank=True)

    class Meta:
        db_table = 'student_promotions'

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.from_class.name} to {self.to_class.name}"
