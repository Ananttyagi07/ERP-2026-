"""
ID Card and Admit Card generation models
"""
from django.db import models
from apps.core.models import TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel


class IDCardSetting(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """ID Card design template"""
    border_color = models.CharField(max_length=7, default='#000000', help_text="Hex color code")
    top_background = models.CharField(max_length=7, default='#FFFFFF')
    card_school_name = models.CharField(max_length=255)
    school_name_font_size = models.IntegerField(default=14)
    school_name_color = models.CharField(max_length=7, default='#000000')
    school_address = models.CharField(max_length=500, blank=True)
    school_address_color = models.CharField(max_length=7, default='#000000')
    id_no_font_size = models.IntegerField(default=12)
    id_no_color = models.CharField(max_length=7, default='#000000')
    id_no_background = models.CharField(max_length=7, default='#FFFFFF')
    title_font_size = models.IntegerField(default=12)
    title_color = models.CharField(max_length=7, default='#000000')
    value_font_size = models.IntegerField(default=11)
    value_color = models.CharField(max_length=7, default='#000000')
    bottom_signature = models.CharField(max_length=255)
    signature_background = models.CharField(max_length=7, default='#FFFFFF')
    signature_color = models.CharField(max_length=7, default='#000000')
    signature_align = models.CharField(max_length=10, choices=[('left', 'Left'), ('center', 'Center'), ('right', 'Right')], default='center')
    card_logo = models.ImageField(upload_to='card_logos/', null=True, blank=True, help_text="Max: 100x110px")

    class Meta:
        db_table = 'id_card_settings'

    def __str__(self):
        return f"ID Card Setting - {self.college.name}"


class AdmitCardSetting(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Admit Card design template"""
    border_color = models.CharField(max_length=7, default='#000000')
    top_background = models.CharField(max_length=7, default='#FFFFFF')
    card_school_name = models.CharField(max_length=255)
    school_name_font_size = models.IntegerField(default=14)
    school_name_color = models.CharField(max_length=7, default='#000000')
    school_address = models.CharField(max_length=500, blank=True)
    school_address_color = models.CharField(max_length=7, default='#000000')
    admit_title_font_size = models.IntegerField(default=16)
    admit_title_color = models.CharField(max_length=7, default='#000000')
    admit_title_background = models.CharField(max_length=7, default='#FFFFFF')
    title_font_size = models.IntegerField(default=12)
    title_color = models.CharField(max_length=7, default='#000000')
    value_font_size = models.IntegerField(default=11)
    value_color = models.CharField(max_length=7, default='#000000')
    exam_title_font_size = models.IntegerField(default=13)
    exam_title_color = models.CharField(max_length=7, default='#000000')
    subject_font_size = models.IntegerField(default=11)
    subject_color = models.CharField(max_length=7, default='#000000')
    bottom_signature = models.CharField(max_length=255)
    signature_background = models.CharField(max_length=7, default='#FFFFFF')
    signature_color = models.CharField(max_length=7, default='#000000')
    signature_align = models.CharField(max_length=10, choices=[('left', 'Left'), ('center', 'Center'), ('right', 'Right')], default='center')
    card_logo = models.ImageField(upload_to='card_logos/', null=True, blank=True)

    class Meta:
        db_table = 'admit_card_settings'

    def __str__(self):
        return f"Admit Card Setting - {self.college.name}"
