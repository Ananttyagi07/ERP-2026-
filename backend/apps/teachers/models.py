"""
Teacher management models
"""
from django.db import models
from apps.core.models import TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel


# NOTE: Department model has been moved to apps/colleges/models.py
# to avoid duplication and maintain proper app structure


class Teacher(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Teacher profile"""
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='teacher_profile')
    department = models.ForeignKey('colleges.Department', on_delete=models.PROTECT, related_name='department_teachers')
    designation = models.ForeignKey('hr.Designation', on_delete=models.PROTECT, related_name='teachers')

    # Basic Info
    national_id = models.CharField(max_length=50, blank=True)
    blood_group = models.CharField(max_length=5, choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')], blank=True)
    religion = models.CharField(max_length=50, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    joining_date = models.DateField()
    present_address = models.TextField(blank=True)
    permanent_address = models.TextField(blank=True)

    # Academic Info
    qualification = models.CharField(max_length=255, blank=True)
    specialization = models.CharField(max_length=255, blank=True)
    experience_years = models.IntegerField(default=0)

    # Other Info
    facebook = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    pinterest = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    resume = models.FileField(upload_to='teachers/resumes/', null=True, blank=True)
    photo = models.ImageField(upload_to='teachers/photos/', null=True, blank=True)
    other_info = models.TextField(blank=True)

    class Meta:
        db_table = 'teachers'

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.department.name}"


class TeacherLecture(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Teacher lecture/class tracking"""
    title = models.CharField(max_length=255)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='lectures')
    class_id = models.ForeignKey('academic.SchoolClass', on_delete=models.CASCADE, related_name='lectures')
    section_id = models.ForeignKey('academic.ClassSection', on_delete=models.CASCADE, related_name='lectures')
    subject_id = models.ForeignKey('academic.Subject', on_delete=models.CASCADE, related_name='lectures')
    lecture_type = models.CharField(max_length=50, choices=[('Theory', 'Theory'), ('Practical', 'Practical'), ('Tutorial', 'Tutorial')])
    lecture_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    note = models.TextField(blank=True)

    class Meta:
        db_table = 'teacher_lectures'

    def __str__(self):
        return f"{self.title} - {self.teacher.user.get_full_name()}"


class Rating(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Teacher and department rating"""
    rating_type = models.CharField(max_length=20, choices=[('Teacher', 'Teacher'), ('Department', 'Department')])
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True, related_name='ratings')
    department = models.ForeignKey('colleges.Department', on_delete=models.CASCADE, null=True, blank=True, related_name='department_ratings')
    rating_value = models.DecimalField(max_digits=3, decimal_places=2, help_text="0.00 to 5.00")
    comment = models.TextField(blank=True)
    rated_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, related_name='ratings_given')

    class Meta:
        db_table = 'ratings'

    def __str__(self):
        if self.rating_type == 'Teacher':
            return f"Rating: {self.teacher.user.get_full_name()} - {self.rating_value}"
        return f"Rating: {self.department.name} - {self.rating_value}"
