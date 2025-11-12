"""Subscription/SaaS models"""
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
