"""Payroll Management models"""
from django.db import models
from apps.core.models import TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel


class SalaryGrade(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Salary grade templates"""
    grade_name = models.CharField(max_length=255)
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    house_rent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    transport_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    medical_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    over_time_hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    provident_fund = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2)
    total_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    gross_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    note = models.TextField(blank=True)

    class Meta:
        db_table = 'salary_grades'

    def save(self, *args, **kwargs):
        self.total_allowance = self.house_rent + self.transport_allowance + self.medical_allowance
        self.total_deduction = self.provident_fund
        self.gross_salary = self.basic_salary + self.total_allowance
        self.net_salary = self.gross_salary - self.total_deduction
        super().save(*args, **kwargs)

    def __str__(self):
        return self.grade_name


class SalaryPayment(TimeStampedModel, CollegeIsolatedModel):
    """Salary payment records"""
    USER_TYPES = [
        ('Teacher', 'Teacher'),
        ('Employee', 'Employee'),
    ]
    SALARY_TYPES = [
        ('Monthly', 'Monthly'),
        ('Hourly', 'Hourly'),
    ]

    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='salary_payments')
    month = models.CharField(max_length=20)
    salary_grade = models.ForeignKey(SalaryGrade, on_delete=models.CASCADE)
    salary_type = models.CharField(max_length=20, choices=SALARY_TYPES)
    total_allowance = models.DecimalField(max_digits=10, decimal_places=2)
    total_deduction = models.DecimalField(max_digits=10, decimal_places=2)
    gross_salary = models.DecimalField(max_digits=10, decimal_places=2)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)
    paid_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, related_name='salaries_paid')

    class Meta:
        db_table = 'salary_payments'
        unique_together = [['user', 'month']]

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.month}"
