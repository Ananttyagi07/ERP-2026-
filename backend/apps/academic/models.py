"""
Academic models (Class, Section, Subject, Syllabus, Study Material)
"""
from django.db import models
from apps.core.models import TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel


class SchoolClass(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """School class/grade"""
    name = models.CharField(max_length=255, help_text="e.g., Grade 1, MCA")
    numeric_name = models.IntegerField(help_text="e.g., 1, 2, 10")
    class_teacher = models.ForeignKey('teachers.Teacher', on_delete=models.SET_NULL, null=True, blank=True, related_name='classes_teaching')
    note = models.TextField(blank=True)

    class Meta:
        db_table = 'school_classes'
        verbose_name = 'Class'
        verbose_name_plural = 'Classes'

    def __str__(self):
        return self.name


class ClassSection(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Section within a class"""
    name = models.CharField(max_length=50, help_text="e.g., A, B, C")
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, related_name='sections')
    section_teacher = models.ForeignKey('teachers.Teacher', on_delete=models.SET_NULL, null=True, blank=True, related_name='sections_teaching')
    note = models.TextField(blank=True)

    class Meta:
        db_table = 'class_sections'

    def __str__(self):
        return f"{self.school_class.name} - {self.name}"


class Subject(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Subject definition"""
    name = models.CharField(max_length=255)
    subject_code = models.CharField(max_length=50, blank=True)
    author = models.CharField(max_length=255, blank=True)
    subject_type = models.CharField(max_length=20, choices=[('Core', 'Core'), ('Elective', 'Elective'), ('Optional', 'Optional')])
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, related_name='subjects')
    teacher = models.ForeignKey('teachers.Teacher', on_delete=models.SET_NULL, null=True, blank=True, related_name='subjects_teaching')
    note = models.TextField(blank=True)

    class Meta:
        db_table = 'subjects'

    def __str__(self):
        return f"{self.name} ({self.school_class.name})"


class Syllabus(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Syllabus for subject"""
    title = models.CharField(max_length=255)
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, related_name='syllabi')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='syllabi')
    session_year = models.CharField(max_length=20, help_text="e.g., 2024-25")
    syllabus_file = models.FileField(upload_to='syllabi/', help_text="Allowed: .pdf, .doc, .docx, .pptx, .txt")
    note = models.TextField(blank=True)

    class Meta:
        db_table = 'syllabi'
        verbose_name_plural = 'Syllabi'

    def __str__(self):
        return f"{self.title} - {self.subject.name}"


class StudyMaterial(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Additional study materials"""
    title = models.CharField(max_length=255)
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, related_name='study_materials')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='study_materials')
    material_file = models.FileField(upload_to='study_materials/')
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'study_materials'

    def __str__(self):
        return self.title
