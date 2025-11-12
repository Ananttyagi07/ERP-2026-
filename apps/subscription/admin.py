"""
Django admin configuration for subscription
"""
from django.contrib import admin
from .models import SubscriptionPlan, Subscription, SubscriptionPayment


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'plan_type', 'price', 'max_students']
    list_filter = ['created_at']
    search_fields = ['name', 'plan_type', 'price']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['college', 'plan', 'status', 'start_date', 'end_date']
    list_filter = ['created_at']
    search_fields = ['college', 'plan', 'status']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


@admin.register(SubscriptionPayment)
class SubscriptionPaymentAdmin(admin.ModelAdmin):
    list_display = ['subscription', 'amount', 'payment_method', 'payment_date']
    list_filter = ['created_at']
    search_fields = ['subscription', 'amount', 'payment_method']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


