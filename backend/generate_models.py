#!/usr/bin/env python3
"""
Script to generate all models for the ERP system
Run this from backend directory: python generate_models.py
"""

MODELS = {
    'apps/superadmin/models.py': '''"""
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
''',

    'apps/templates/models.py': '''"""
Template management models (SMS & Email)
"""
from django.db import models
from apps.core.models import TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel


class SMSTemplate(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """SMS Template with dynamic tags"""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    message_body = models.TextField(help_text="Use tags: {name}, {email}, {phone}, {school}, {class}, {section}, {roll}, {subject}")
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'sms_templates'

    def __str__(self):
        return self.name


class EmailTemplate(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Email Template with dynamic tags"""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    subject = models.CharField(max_length=255)
    message_body = models.TextField(help_text="Use tags: {name}, {email}, {phone}, {school}, {class}, {section}, {roll}, {subject}")
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'email_templates'

    def __str__(self):
        return self.name
''',

    'apps/front_office/models.py': '''"""
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
''',

    'apps/hr/models.py': '''"""
Human Resource models (Designation, Employee)
"""
from django.db import models
from apps.core.models import TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel


class Designation(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Job designation/position"""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'designations'

    def __str__(self):
        return self.name


class Employee(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Employee profile (3-tab form: Basic, Academic, Other Info)"""
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='employee_profile')

    # Basic Info
    designation = models.ForeignKey(Designation, on_delete=models.PROTECT, related_name='employees')
    national_id = models.CharField(max_length=50, blank=True)
    blood_group = models.CharField(max_length=5, choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')], blank=True)
    religion = models.CharField(max_length=50, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    joining_date = models.DateField()
    present_address = models.TextField(blank=True)
    permanent_address = models.TextField(blank=True)

    # Academic Info
    qualification = models.CharField(max_length=255, blank=True)
    experience_years = models.IntegerField(default=0)

    # Other Info
    facebook = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    pinterest = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    resume = models.FileField(upload_to='employees/resumes/', null=True, blank=True)
    photo = models.ImageField(upload_to='employees/photos/', null=True, blank=True)
    other_info = models.TextField(blank=True)

    class Meta:
        db_table = 'employees'

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.designation.name}"
''',

    'apps/teachers/models.py': '''"""
Teacher management models
"""
from django.db import models
from apps.core.models import TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel


class Department(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Academic department"""
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    head = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='department_head_of')
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'departments'
        unique_together = [['college', 'code']]

    def __str__(self):
        return self.name


class Teacher(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Teacher profile"""
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='teacher_profile')
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='teachers')
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
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True, related_name='ratings')
    rating_value = models.DecimalField(max_digits=3, decimal_places=2, help_text="0.00 to 5.00")
    comment = models.TextField(blank=True)
    rated_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, related_name='ratings_given')

    class Meta:
        db_table = 'ratings'

    def __str__(self):
        if self.rating_type == 'Teacher':
            return f"Rating: {self.teacher.user.get_full_name()} - {self.rating_value}"
        return f"Rating: {self.department.name} - {self.rating_value}"
''',

    'apps/leave_management/models.py': '''"""
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
''',

    'apps/academic/models.py': '''"""
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
''',

    'apps/live_classes/models.py': '''"""
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
''',

    'apps/students/models.py': '''"""
Student management models
"""
from django.db import models
from apps.core.models import TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel


class Student(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Student profile"""
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='student_profile')

    # Academic Info
    school_class = models.ForeignKey('academic.SchoolClass', on_delete=models.PROTECT, related_name='students')
    section = models.ForeignKey('academic.ClassSection', on_delete=models.PROTECT, related_name='students')
    roll_number = models.CharField(max_length=50)
    registration_number = models.CharField(max_length=100, unique=True)
    admission_date = models.DateField()

    # Basic Info
    national_id = models.CharField(max_length=50, blank=True)
    blood_group = models.CharField(max_length=5, choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')], blank=True)
    religion = models.CharField(max_length=50, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    present_address = models.TextField(blank=True)
    permanent_address = models.TextField(blank=True)

    # Additional Info
    photo = models.ImageField(upload_to='students/photos/', null=True, blank=True)
    other_info = models.TextField(blank=True)

    class Meta:
        db_table = 'students'
        unique_together = [['college', 'roll_number', 'school_class', 'section']]

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.roll_number}"


class StudentParent(TimeStampedModel, SoftDeleteModel):
    """Relationship between student and guardian"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='parents')
    guardian = models.ForeignKey('guardians.Guardian', on_delete=models.CASCADE, related_name='children')
    relationship = models.CharField(max_length=50, choices=[('Father', 'Father'), ('Mother', 'Mother'), ('Guardian', 'Guardian'), ('Other', 'Other')])
    is_primary = models.BooleanField(default=False, help_text="Primary contact")

    class Meta:
        db_table = 'student_parents'
        unique_together = [['student', 'guardian']]

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.guardian.user.get_full_name()} ({self.relationship})"
''',

    'apps/guardians/models.py': '''"""
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
''',
}


def generate_all_models():
    """Write all model files"""
    import os

    for filepath, content in MODELS.items():
        # Create directories if they don't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, 'w') as f:
            f.write(content)

        print(f"✓ Created: {filepath}")

    print(f"\n✅ Generated {len(MODELS)} model files successfully!")


if __name__ == '__main__':
    generate_all_models()
