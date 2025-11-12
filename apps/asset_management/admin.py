"""
Django admin configuration for asset_management
"""
from django.contrib import admin
from .models import Vendor, Store, AssetCategory, AssetItem, AssetPurchase, AssetIssue


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'contact_name']
    list_filter = ['created_at']
    search_fields = ['name', 'email', 'phone']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['name', 'store_code', 'description']
    list_filter = ['created_at']
    search_fields = ['name', 'store_code', 'description']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


@admin.register(AssetCategory)
class AssetCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


@admin.register(AssetItem)
class AssetItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'product_code', 'item_type', 'category', 'store']
    list_filter = ['created_at']
    search_fields = ['name', 'product_code', 'item_type']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


@admin.register(AssetPurchase)
class AssetPurchaseAdmin(admin.ModelAdmin):
    list_display = ['item', 'quantity', 'unit_price', 'vendor', 'purchase_date']
    list_filter = ['created_at']
    search_fields = ['item', 'quantity', 'unit_price']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


@admin.register(AssetIssue)
class AssetIssueAdmin(admin.ModelAdmin):
    list_display = ['item', 'quantity', 'issued_to_type', 'issue_date']
    list_filter = ['created_at']
    search_fields = ['item', 'quantity', 'issued_to_type']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


