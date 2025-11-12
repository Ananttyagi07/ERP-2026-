"""
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
