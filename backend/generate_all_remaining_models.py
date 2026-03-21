#!/usr/bin/env python3
"""
Generate ALL remaining models for the complete ERP system
35 new models across 9 modules
"""

MODELS = {
    # ============================================================================
    # STUDENT MANAGEMENT MODELS
    # ============================================================================
    'apps/student_management/models.py': '''"""
Student Management models (enhanced student features)
"""
from django.db import models
from apps.core.models import TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel


class StudentType(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Student type (Undergraduate, Postgraduate, etc.)"""
    name = models.CharField(max_length=255, help_text="e.g., Undergraduate, Postgraduate")
    note = models.TextField(blank=True)

    class Meta:
        db_table = 'student_types'
        unique_together = [['college', 'name']]

    def __str__(self):
        return self.name


class OnlineAdmission(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Online admission applications"""
    student_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    school_class = models.ForeignKey('academic.SchoolClass', on_delete=models.CASCADE, related_name='online_admissions')
    photo = models.ImageField(upload_to='online_admissions/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending')
    application_data = models.JSONField(default=dict, help_text="Full application form data")

    class Meta:
        db_table = 'online_admissions'

    def __str__(self):
        return f"{self.student_name} - {self.status}"


class StudentActivity(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Student activities tracking"""
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='activities')
    school_class = models.ForeignKey('academic.SchoolClass', on_delete=models.CASCADE)
    section = models.ForeignKey('academic.ClassSection', on_delete=models.CASCADE)
    activity = models.TextField()
    activity_date = models.DateField()

    class Meta:
        db_table = 'student_activities'

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.activity_date}"
''',

    # ============================================================================
    # ATTENDANCE MODELS
    # ============================================================================
    'apps/attendance/models.py': '''"""
Attendance tracking models
"""
from django.db import models
from apps.core.models import TimeStampedModel, CollegeIsolatedModel


class StudentAttendance(TimeStampedModel, CollegeIsolatedModel):
    """Daily student attendance"""
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='attendances')
    school_class = models.ForeignKey('academic.SchoolClass', on_delete=models.CASCADE)
    section = models.ForeignKey('academic.ClassSection', on_delete=models.CASCADE)
    attendance_date = models.DateField()
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Late', 'Late'), ('Absent', 'Absent')])
    marked_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, related_name='student_attendances_marked')

    class Meta:
        db_table = 'student_attendances'
        unique_together = [['student', 'attendance_date']]
        indexes = [models.Index(fields=['attendance_date', 'school_class', 'section'])]

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.attendance_date} - {self.status}"


class TeacherAttendance(TimeStampedModel, CollegeIsolatedModel):
    """Daily teacher attendance"""
    teacher = models.ForeignKey('teachers.Teacher', on_delete=models.CASCADE, related_name='attendances')
    attendance_date = models.DateField()
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Late', 'Late'), ('Absent', 'Absent')])
    marked_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, related_name='teacher_attendances_marked')

    class Meta:
        db_table = 'teacher_attendances'
        unique_together = [['teacher', 'attendance_date']]

    def __str__(self):
        return f"{self.teacher.user.get_full_name()} - {self.attendance_date} - {self.status}"


class EmployeeAttendance(TimeStampedModel, CollegeIsolatedModel):
    """Daily employee attendance"""
    employee = models.ForeignKey('hr.Employee', on_delete=models.CASCADE, related_name='attendances')
    attendance_date = models.DateField()
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Late', 'Late'), ('Absent', 'Absent')])
    marked_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, related_name='employee_attendances_marked')

    class Meta:
        db_table = 'employee_attendances'
        unique_together = [['employee', 'attendance_date']]

    def __str__(self):
        return f"{self.employee.user.get_full_name()} - {self.attendance_date} - {self.status}"


class AbsentEmailLog(TimeStampedModel, CollegeIsolatedModel):
    """Log of absent notification emails sent"""
    receiver_type = models.CharField(max_length=50, choices=[('Student', 'Student'), ('Teacher', 'Teacher'), ('Employee', 'Employee'), ('Guardian', 'Guardian')])
    receiver_email = models.EmailField()
    subject = models.CharField(max_length=255)
    body = models.TextField()
    absent_date = models.DateField()
    template = models.ForeignKey('templates.EmailTemplate', on_delete=models.SET_NULL, null=True, blank=True)
    sent_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'absent_email_logs'

    def __str__(self):
        return f"{self.receiver_type} - {self.receiver_email} - {self.absent_date}"


class AbsentSMSLog(TimeStampedModel, CollegeIsolatedModel):
    """Log of absent notification SMS sent"""
    receiver_type = models.CharField(max_length=50, choices=[('Student', 'Student'), ('Teacher', 'Teacher'), ('Employee', 'Employee'), ('Guardian', 'Guardian')])
    receiver_phone = models.CharField(max_length=20)
    message = models.TextField()
    absent_date = models.DateField()
    template = models.ForeignKey('templates.SMSTemplate', on_delete=models.SET_NULL, null=True, blank=True)
    gateway = models.CharField(max_length=100)
    sent_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'absent_sms_logs'

    def __str__(self):
        return f"{self.receiver_type} - {self.receiver_phone} - {self.absent_date}"
''',

    # ============================================================================
    # CARD GENERATION MODELS
    # ============================================================================
    'apps/card_generation/models.py': '''"""
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
''',

    # ============================================================================
    # ONLINE EXAM MODELS
    # ============================================================================
    'apps/online_exam/models.py': '''"""
Online Exam models
"""
from django.db import models
from apps.core.models import TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel


class ExamInstruction(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Reusable exam instructions"""
    title = models.CharField(max_length=255)
    instruction = models.TextField()

    class Meta:
        db_table = 'exam_instructions'

    def __str__(self):
        return self.title


class QuestionBank(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Question bank for online exams"""
    QUESTION_TYPES = [
        ('Multiple Choice', 'Multiple Choice'),
        ('True/False', 'True/False'),
        ('Short Answer', 'Short Answer'),
    ]
    QUESTION_LEVELS = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]

    school_class = models.ForeignKey('academic.SchoolClass', on_delete=models.CASCADE)
    section = models.ForeignKey('academic.ClassSection', on_delete=models.CASCADE)
    subject = models.ForeignKey('academic.Subject', on_delete=models.CASCADE)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    question_level = models.CharField(max_length=10, choices=QUESTION_LEVELS)
    question = models.TextField()
    option_a = models.CharField(max_length=500, blank=True)
    option_b = models.CharField(max_length=500, blank=True)
    option_c = models.CharField(max_length=500, blank=True)
    option_d = models.CharField(max_length=500, blank=True)
    correct_answer = models.CharField(max_length=500)
    mark = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        db_table = 'question_bank'

    def __str__(self):
        return f"{self.subject.name} - {self.question_type}"


class OnlineExam(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Online exam configuration"""
    exam_title = models.CharField(max_length=255)
    school_class = models.ForeignKey('academic.SchoolClass', on_delete=models.CASCADE)
    section = models.ForeignKey('academic.ClassSection', on_delete=models.CASCADE)
    subject = models.ForeignKey('academic.Subject', on_delete=models.CASCADE)
    instruction = models.ForeignKey(ExamInstruction, on_delete=models.SET_NULL, null=True, blank=True)
    exam_date = models.DateField()
    exam_time = models.TimeField()
    duration_minutes = models.IntegerField(help_text="Duration in minutes")
    total_mark = models.DecimalField(max_digits=6, decimal_places=2)
    passing_mark = models.DecimalField(max_digits=6, decimal_places=2)
    publish_status = models.BooleanField(default=False)
    questions = models.ManyToManyField(QuestionBank, related_name='exams')

    class Meta:
        db_table = 'online_exams'

    def __str__(self):
        return f"{self.exam_title} - {self.exam_date}"


class OnlineExamResult(TimeStampedModel, CollegeIsolatedModel):
    """Online exam results"""
    exam = models.ForeignKey(OnlineExam, on_delete=models.CASCADE, related_name='results')
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    answers = models.JSONField(default=dict, help_text="Student answers")
    obtained_mark = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(max_length=10, choices=[('Pass', 'Pass'), ('Fail', 'Fail')])
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'online_exam_results'
        unique_together = [['exam', 'student']]

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.exam.exam_title} - {self.obtained_mark}"
''',

    # ============================================================================
    # EXAM MANAGEMENT MODELS
    # ============================================================================
    'apps/exam_management/models.py': '''"""
Exam Management models
"""
from django.db import models
from apps.core.models import TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel


class Grade(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Grading system"""
    grade_name = models.CharField(max_length=10, help_text="e.g., A+, A, B+")
    point = models.DecimalField(max_digits=4, decimal_places=2)
    mark_from = models.DecimalField(max_digits=5, decimal_places=2)
    mark_to = models.DecimalField(max_digits=5, decimal_places=2)
    note = models.TextField(blank=True)

    class Meta:
        db_table = 'grades'
        ordering = ['-mark_from']

    def __str__(self):
        return f"{self.grade_name} ({self.mark_from}-{self.mark_to})"


class ExamTerm(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Exam terms (e.g., Midterm, Final)"""
    name = models.CharField(max_length=255)
    note = models.TextField(blank=True)

    class Meta:
        db_table = 'exam_terms'
        unique_together = [['college', 'name']]

    def __str__(self):
        return self.name


class ExamSchedule(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Exam schedule for subjects"""
    exam_term = models.ForeignKey(ExamTerm, on_delete=models.CASCADE, related_name='schedules')
    school_class = models.ForeignKey('academic.SchoolClass', on_delete=models.CASCADE)
    section = models.ForeignKey('academic.ClassSection', on_delete=models.CASCADE)
    subject = models.ForeignKey('academic.Subject', on_delete=models.CASCADE)
    exam_date = models.DateField()
    exam_time = models.TimeField()
    duration_minutes = models.IntegerField()
    room_no = models.CharField(max_length=50, blank=True)
    total_mark = models.DecimalField(max_digits=6, decimal_places=2)
    passing_mark = models.DecimalField(max_digits=6, decimal_places=2)
    note = models.TextField(blank=True)

    class Meta:
        db_table = 'exam_schedules'
        unique_together = [['exam_term', 'school_class', 'section', 'subject']]

    def __str__(self):
        return f"{self.exam_term.name} - {self.subject.name} - {self.exam_date}"


class ExamSuggestion(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Exam suggestions/study materials"""
    exam_term = models.ForeignKey(ExamTerm, on_delete=models.CASCADE)
    school_class = models.ForeignKey('academic.SchoolClass', on_delete=models.CASCADE)
    section = models.ForeignKey('academic.ClassSection', on_delete=models.CASCADE)
    subject = models.ForeignKey('academic.Subject', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    suggestion_file = models.FileField(upload_to='exam_suggestions/')

    class Meta:
        db_table = 'exam_suggestions'

    def __str__(self):
        return f"{self.title} - {self.subject.name}"


class ExamAttendanceRecord(TimeStampedModel, CollegeIsolatedModel):
    """Exam attendance tracking"""
    exam_schedule = models.ForeignKey(ExamSchedule, on_delete=models.CASCADE, related_name='attendances')
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])
    marked_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'exam_attendance_records'
        unique_together = [['exam_schedule', 'student']]

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.exam_schedule.subject.name} - {self.status}"
''',

    # ============================================================================
    # MARKS MANAGEMENT MODELS
    # ============================================================================
    'apps/marks/models.py': '''"""
Marks and Results Management models
"""
from django.db import models
from apps.core.models import TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel


class ExamMark(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Student exam marks"""
    exam_schedule = models.ForeignKey('exam_management.ExamSchedule', on_delete=models.CASCADE, related_name='marks')
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    written_mark = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    tutorial_mark = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    practical_mark = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    viva_mark = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    total_mark = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    grade = models.ForeignKey('exam_management.Grade', on_delete=models.SET_NULL, null=True, blank=True)
    attendance_status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')], default='Present')
    note = models.TextField(blank=True)

    class Meta:
        db_table = 'exam_marks'
        unique_together = [['exam_schedule', 'student']]

    def save(self, *args, **kwargs):
        self.total_mark = self.written_mark + self.tutorial_mark + self.practical_mark + self.viva_mark
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.exam_schedule.subject.name} - {self.total_mark}"


class MarkDistribution(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Mark distribution configuration"""
    exam_term = models.ForeignKey('exam_management.ExamTerm', on_delete=models.CASCADE)
    school_class = models.ForeignKey('academic.SchoolClass', on_delete=models.CASCADE)
    subject = models.ForeignKey('academic.Subject', on_delete=models.CASCADE)
    written_total = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    tutorial_total = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    practical_total = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    viva_total = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    class Meta:
        db_table = 'mark_distributions'
        unique_together = [['exam_term', 'school_class', 'subject']]

    def __str__(self):
        return f"{self.exam_term.name} - {self.subject.name}"


class ResultCard(TimeStampedModel, CollegeIsolatedModel):
    """Generated result cards"""
    exam_term = models.ForeignKey('exam_management.ExamTerm', on_delete=models.CASCADE)
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    school_class = models.ForeignKey('academic.SchoolClass', on_delete=models.CASCADE)
    section = models.ForeignKey('academic.ClassSection', on_delete=models.CASCADE)
    total_marks = models.DecimalField(max_digits=7, decimal_places=2)
    obtained_marks = models.DecimalField(max_digits=7, decimal_places=2)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    overall_grade = models.ForeignKey('exam_management.Grade', on_delete=models.SET_NULL, null=True)
    result_status = models.CharField(max_length=10, choices=[('Pass', 'Pass'), ('Fail', 'Fail')])
    merit_position = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'result_cards'
        unique_together = [['exam_term', 'student']]

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.exam_term.name} - {self.percentage}%"


class MarkEmailLog(TimeStampedModel, CollegeIsolatedModel):
    """Log of mark notification emails"""
    exam_schedule = models.ForeignKey('exam_management.ExamSchedule', on_delete=models.CASCADE)
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    receiver_email = models.EmailField()
    subject = models.CharField(max_length=255)
    body = models.TextField()
    template = models.ForeignKey('templates.EmailTemplate', on_delete=models.SET_NULL, null=True, blank=True)
    sent_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'mark_email_logs'

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.receiver_email}"


class MarkSMSLog(TimeStampedModel, CollegeIsolatedModel):
    """Log of mark notification SMS"""
    exam_schedule = models.ForeignKey('exam_management.ExamSchedule', on_delete=models.CASCADE)
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    receiver_phone = models.CharField(max_length=20)
    message = models.TextField()
    template = models.ForeignKey('templates.SMSTemplate', on_delete=models.SET_NULL, null=True, blank=True)
    gateway = models.CharField(max_length=100)
    sent_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'mark_sms_logs'

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.receiver_phone}"


class ResultEmailLog(TimeStampedModel, CollegeIsolatedModel):
    """Log of result notification emails"""
    exam_term = models.ForeignKey('exam_management.ExamTerm', on_delete=models.CASCADE)
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    receiver_email = models.EmailField()
    subject = models.CharField(max_length=255)
    body = models.TextField()
    template = models.ForeignKey('templates.EmailTemplate', on_delete=models.SET_NULL, null=True, blank=True)
    sent_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'result_email_logs'

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.receiver_email}"


class ResultSMSLog(TimeStampedModel, CollegeIsolatedModel):
    """Log of result notification SMS"""
    exam_term = models.ForeignKey('exam_management.ExamTerm', on_delete=models.CASCADE)
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    receiver_phone = models.CharField(max_length=20)
    message = models.TextField()
    template = models.ForeignKey('templates.SMSTemplate', on_delete=models.SET_NULL, null=True, blank=True)
    gateway = models.CharField(max_length=100)
    sent_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'result_sms_logs'

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.receiver_phone}"
''',

    # ============================================================================
    # PROMOTION MODELS
    # ============================================================================
    'apps/promotion/models.py': '''"""
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
''',

    # ============================================================================
    # CERTIFICATE MODELS
    # ============================================================================
    'apps/certificates/models.py': '''"""
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
''',

    # ============================================================================
    # INVENTORY MODELS
    # ============================================================================
    'apps/inventory/models.py': '''"""
Inventory Management models
"""
from django.db import models
from apps.core.models import TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel


class Supplier(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Product suppliers"""
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    address = models.TextField()

    class Meta:
        db_table = 'suppliers'

    def __str__(self):
        return self.name


class Warehouse(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Storage warehouses"""
    title = models.CharField(max_length=255)
    address = models.TextField()

    class Meta:
        db_table = 'warehouses'

    def __str__(self):
        return self.title


class InventoryCategory(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Product categories"""
    name = models.CharField(max_length=255)
    note = models.TextField(blank=True)

    class Meta:
        db_table = 'inventory_categories'
        unique_together = [['college', 'name']]

    def __str__(self):
        return self.name


class Product(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Products/Items"""
    name = models.CharField(max_length=255)
    category = models.ForeignKey(InventoryCategory, on_delete=models.CASCADE, related_name='products')
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    unit = models.CharField(max_length=50, help_text="e.g., Piece, Box, Kg")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'products'

    def __str__(self):
        return f"{self.name} ({self.quantity} {self.unit})"


class Purchase(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Purchase records"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='purchases')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    purchase_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    purchased_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'purchases'

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Purchase: {self.product.name} - {self.quantity} units"


class Sale(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Sales records"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sales')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    sale_date = models.DateField()
    customer_name = models.CharField(max_length=255)
    customer_phone = models.CharField(max_length=20, blank=True)
    invoice_no = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    sold_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'sales'

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Sale: {self.product.name} - Invoice: {self.invoice_no}"


class ProductIssue(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Product issue/return tracking"""
    ISSUE_TYPES = [
        ('Issue', 'Issue'),
        ('Return', 'Return'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='issues')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    issue_type = models.CharField(max_length=10, choices=ISSUE_TYPES)
    quantity = models.IntegerField()
    issue_to = models.CharField(max_length=255, help_text="Department, Person, or Class")
    issue_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    note = models.TextField(blank=True)
    issued_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'product_issues'

    def __str__(self):
        return f"{self.issue_type}: {self.product.name} - {self.quantity} units"
''',
}

# Write the models
print("🚀 Generating ALL remaining models...")
print("=" * 70)

import os

for filepath, content in MODELS.items():
    # Ensure directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, 'w') as f:
        f.write(content)
    print(f"✓ {filepath}")

print("\n" + "=" * 70)
print("✅ ALL 35 MODELS CREATED SUCCESSFULLY!")
print("=" * 70)
print("\nModules Created:")
print("  1. Student Management (3 models)")
print("  2. Attendance (5 models)")
print("  3. Card Generation (2 models)")
print("  4. Online Exam (4 models)")
print("  5. Exam Management (5 models)")
print("  6. Marks Management (7 models)")
print("  7. Promotion (1 model)")
print("  8. Certificate (2 models)")
print("  9. Inventory (7 models)")
print("\nTotal: 35 new models across 9 modules")
print("\nNext: Create __init__.py and apps.py for all modules")
