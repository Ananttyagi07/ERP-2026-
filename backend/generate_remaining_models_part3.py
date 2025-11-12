#!/usr/bin/env python3
"""Generate remaining Superadmin models - Part 3 (Payroll, Accounting, etc.)"""

MODELS = {
    # Payroll
    'apps/payroll/models.py': '''"""Payroll Management models"""
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
''',

    # Accounting (Complex module with 10+ models)
    'apps/accounting/models.py': '''"""Accounting & Finance models"""
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
''',

    # Media Gallery
    'apps/media_gallery/models.py': '''"""Media Gallery models"""
from django.db import models
from apps.core.models import TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel


class Gallery(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Photo galleries/albums"""
    title = models.CharField(max_length=255)
    note = models.TextField(blank=True)
    is_view_on_web = models.BooleanField(default=False)

    class Meta:
        db_table = 'galleries'
        verbose_name_plural = 'galleries'

    def __str__(self):
        return self.title


class GalleryImage(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Images in galleries"""
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='gallery/')
    caption = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'gallery_images'

    def __str__(self):
        return f"{self.gallery.title} - {self.caption}"
''',

    # Frontend CMS
    'apps/frontend_cms/models.py': '''"""Frontend CMS models"""
from django.db import models
from apps.core.models import TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel


class FrontendPage(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Custom frontend pages"""
    LOCATION_CHOICES = [
        ('Header', 'Header'),
        ('Footer', 'Footer'),
        ('Sidebar', 'Sidebar'),
    ]

    location = models.CharField(max_length=20, choices=LOCATION_CHOICES)
    title = models.CharField(max_length=255)
    url_slug = models.SlugField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='pages/', null=True, blank=True)

    class Meta:
        db_table = 'frontend_pages'
        unique_together = [['college', 'url_slug']]

    def __str__(self):
        return self.title


class Slider(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Homepage sliders"""
    image = models.ImageField(upload_to='sliders/')
    caption = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'sliders'

    def __str__(self):
        return self.caption or f"Slider {self.id}"


class AboutSchool(TimeStampedModel, CollegeIsolatedModel):
    """About school content (one per college)"""
    content = models.TextField()
    image = models.ImageField(upload_to='about/', null=True, blank=True)

    class Meta:
        db_table = 'about_school'

    def __str__(self):
        return f"About {self.college.name}"
''',

    # Miscellaneous
    'apps/miscellaneous/models.py': '''"""Miscellaneous models (Awards, Todo, FAQ)"""
from django.db import models
from apps.core.models import TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel


class Award(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Awards given to users"""
    USER_TYPES = [
        ('Student', 'Student'),
        ('Teacher', 'Teacher'),
        ('Employee', 'Employee'),
    ]

    academic_year = models.CharField(max_length=20)
    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    winner = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='awards')
    title = models.CharField(max_length=255)
    gift = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    note = models.TextField(blank=True)

    class Meta:
        db_table = 'awards'

    def __str__(self):
        return f"{self.title} - {self.winner.get_full_name()}"


class Todo(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Todo/task management"""
    USER_TYPES = [
        ('Teacher', 'Teacher'),
        ('Employee', 'Employee'),
        ('Admin', 'Admin'),
    ]
    WORK_STATUS = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    assign_to = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='assigned_todos')
    title = models.CharField(max_length=255)
    date = models.DateField()
    work_status = models.CharField(max_length=20, choices=WORK_STATUS, default='Pending')
    description = models.TextField(blank=True)
    comment = models.TextField(blank=True)

    class Meta:
        db_table = 'todos'

    def __str__(self):
        return self.title


class FAQ(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Frequently Asked Questions"""
    title = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        db_table = 'faqs'

    def __str__(self):
        return self.title
''',

    # Subscription/SaaS
    'apps/subscription/models.py': '''"""Subscription/SaaS models"""
from django.db import models
from apps.core.models import TimeStampedModel, SoftDeleteModel


class SubscriptionPlan(TimeStampedModel, SoftDeleteModel):
    """SaaS subscription plans (global, not college-specific)"""
    PLAN_TYPES = [
        ('Free', 'Free'),
        ('Basic', 'Basic'),
        ('Pro', 'Pro'),
        ('Enterprise', 'Enterprise'),
    ]

    name = models.CharField(max_length=255)
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    billing_cycle = models.CharField(max_length=20, help_text="Monthly, Yearly, etc.")
    max_students = models.IntegerField()
    max_teachers = models.IntegerField()
    features = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'subscription_plans'

    def __str__(self):
        return f"{self.name} - ₹{self.price}/{self.billing_cycle}"


class Subscription(TimeStampedModel):
    """College subscriptions (tracks which plan each college is on)"""
    SUBSCRIPTION_STATUS = [
        ('Active', 'Active'),
        ('Expired', 'Expired'),
        ('Cancelled', 'Cancelled'),
        ('Trial', 'Trial'),
    ]

    college = models.ForeignKey('colleges.College', on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=SUBSCRIPTION_STATUS, default='Trial')
    start_date = models.DateField()
    end_date = models.DateField()
    is_auto_renew = models.BooleanField(default=True)

    class Meta:
        db_table = 'subscriptions'

    def __str__(self):
        return f"{self.college.name} - {self.plan.name}"


class SubscriptionPayment(TimeStampedModel):
    """Subscription payment records"""
    PAYMENT_STATUS = [
        ('Success', 'Success'),
        ('Pending', 'Pending'),
        ('Failed', 'Failed'),
    ]

    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    payment_date = models.DateField()
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS)
    transaction_id = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'subscription_payments'

    def __str__(self):
        return f"{self.subscription.college.name} - ₹{self.amount}"
''',
}

print("🚀 Generating remaining models (Part 3)...")
print("=" * 70)

for filepath, content in MODELS.items():
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"✓ {filepath}")

print("\n✅ Part 3 Complete!")
print("Models created: Payroll, Accounting, Media Gallery, Frontend CMS, Miscellaneous, Subscription")
print("\n" + "=" * 70)
print("🎉 ALL SUPERADMIN MODELS COMPLETE!")
print("=" * 70)
print("\nTotal new models: ~50")
print("Next: Generate serializers, views, URLs, admin...")
