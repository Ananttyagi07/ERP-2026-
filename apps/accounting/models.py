"""Accounting & Finance models"""
from django.db import models
from apps.core.models import TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel


class Discount(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Fee discount types"""
    DISCOUNT_TYPES = [
        ('Percentage', 'Percentage'),
        ('Fixed Amount', 'Fixed Amount'),
    ]

    title = models.CharField(max_length=255)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.TextField(blank=True)

    class Meta:
        db_table = 'discounts'

    def __str__(self):
        return self.title


class FeeType(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Types of fees"""
    FEE_TYPE_CHOICES = [
        ('Tuition Fee', 'Tuition Fee'),
        ('Exam Fee', 'Exam Fee'),
        ('Library Fee', 'Library Fee'),
        ('Transport Fee', 'Transport Fee'),
        ('Sports Fee', 'Sports Fee'),
        ('Other', 'Other'),
    ]

    fee_type = models.CharField(max_length=50, choices=FEE_TYPE_CHOICES)
    title = models.CharField(max_length=255)
    note = models.TextField(blank=True)

    class Meta:
        db_table = 'fee_types'

    def __str__(self):
        return self.title


class Invoice(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Fee invoices"""
    PAID_STATUS_CHOICES = [
        ('Paid', 'Paid'),
        ('Partial', 'Partial'),
        ('Unpaid', 'Unpaid'),
    ]

    invoice_number = models.CharField(max_length=100, unique=True)
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='invoices')
    school_class = models.ForeignKey('academic.SchoolClass', on_delete=models.CASCADE)
    fee_type = models.ForeignKey(FeeType, on_delete=models.CASCADE)
    month = models.CharField(max_length=20)
    gross_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    due_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paid_status = models.CharField(max_length=20, choices=PAID_STATUS_CHOICES, default='Unpaid')
    note = models.TextField(blank=True)

    class Meta:
        db_table = 'invoices'

    def save(self, *args, **kwargs):
        self.due_amount = self.net_amount - self.paid_amount
        if self.paid_amount >= self.net_amount:
            self.paid_status = 'Paid'
        elif self.paid_amount > 0:
            self.paid_status = 'Partial'
        else:
            self.paid_status = 'Unpaid'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.invoice_number} - {self.student.user.get_full_name()}"


class Payment(TimeStampedModel, CollegeIsolatedModel):
    """Fee payments"""
    PAYMENT_METHODS = [
        ('Cash', 'Cash'),
        ('Bank Transfer', 'Bank Transfer'),
        ('Cheque', 'Cheque'),
        ('Online', 'Online'),
    ]

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    reference = models.CharField(max_length=255, blank=True)
    note = models.TextField(blank=True)
    received_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'payments'

    def __str__(self):
        return f"{self.invoice.invoice_number} - ₹{self.amount}"


class IncomeHead(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Income categories"""
    name = models.CharField(max_length=255)
    note = models.TextField(blank=True)

    class Meta:
        db_table = 'income_heads'
        unique_together = [['college', 'name']]

    def __str__(self):
        return self.name


class Income(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Income records"""
    INCOME_METHODS = [
        ('Cash', 'Cash'),
        ('Bank Transfer', 'Bank Transfer'),
        ('Cheque', 'Cheque'),
        ('Online', 'Online'),
    ]

    session_year = models.CharField(max_length=20)
    income_head = models.ForeignKey(IncomeHead, on_delete=models.CASCADE, related_name='incomes')
    income_method = models.CharField(max_length=20, choices=INCOME_METHODS)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    note = models.TextField(blank=True)

    class Meta:
        db_table = 'incomes'

    def __str__(self):
        return f"{self.income_head.name} - ₹{self.amount}"


class ExpenditureHead(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Expenditure categories"""
    name = models.CharField(max_length=255)
    note = models.TextField(blank=True)

    class Meta:
        db_table = 'expenditure_heads'
        unique_together = [['college', 'name']]

    def __str__(self):
        return self.name


class Expenditure(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Expenditure records"""
    EXPENDITURE_METHODS = [
        ('Cash', 'Cash'),
        ('Bank Transfer', 'Bank Transfer'),
        ('Cheque', 'Cheque'),
        ('Online', 'Online'),
    ]

    session_year = models.CharField(max_length=20)
    expenditure_head = models.ForeignKey(ExpenditureHead, on_delete=models.CASCADE, related_name='expenditures')
    expenditure_method = models.CharField(max_length=20, choices=EXPENDITURE_METHODS)
    reference = models.CharField(max_length=255, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    note = models.TextField(blank=True)

    class Meta:
        db_table = 'expenditures'

    def __str__(self):
        return f"{self.expenditure_head.name} - ₹{self.amount}"
