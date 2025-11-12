"""
Django admin configuration for accounting
"""
from django.contrib import admin
from .models import Discount, FeeType, Invoice, Payment, IncomeHead, Income, ExpenditureHead, Expenditure


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['title', 'discount_type', 'amount']
    list_filter = ['created_at']
    search_fields = ['title', 'discount_type']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


@admin.register(FeeType)
class FeeTypeAdmin(admin.ModelAdmin):
    list_display = ['fee_type', 'title']
    list_filter = ['created_at']
    search_fields = ['title', 'fee_type']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'student', 'gross_amount', 'net_amount', 'paid_status']
    list_filter = ['created_at']
    search_fields = ['invoice_number', 'student', 'gross_amount']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['invoice', 'amount', 'payment_method', 'payment_date']
    list_filter = ['created_at']
    search_fields = ['invoice', 'amount', 'payment_method']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


@admin.register(IncomeHead)
class IncomeHeadAdmin(admin.ModelAdmin):
    list_display = ['head_name', 'description']
    list_filter = ['created_at']
    search_fields = ['head_name', 'description']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ['income_head', 'amount', 'date']
    list_filter = ['created_at']
    search_fields = ['income_head', 'amount', 'date']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


@admin.register(ExpenditureHead)
class ExpenditureHeadAdmin(admin.ModelAdmin):
    list_display = ['head_name', 'description']
    list_filter = ['created_at']
    search_fields = ['head_name', 'description']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


@admin.register(Expenditure)
class ExpenditureAdmin(admin.ModelAdmin):
    list_display = ['expenditure_head', 'amount', 'date']
    list_filter = ['created_at']
    search_fields = ['expenditure_head', 'amount', 'date']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


