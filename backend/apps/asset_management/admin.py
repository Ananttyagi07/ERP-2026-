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
    list_display = ['name', 'store_keeper', 'phone']
    list_filter = ['created_at']
    search_fields = ['name', 'store_keeper', 'phone']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


@admin.register(AssetCategory)
class AssetCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['created_at']
    search_fields = ['name']
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
    list_display = ['asset', 'quantity', 'unit_price', 'vendor', 'purchase_date']
    list_filter = ['created_at', 'purchase_date']
    search_fields = ['asset__name', 'vendor__name']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


@admin.register(AssetIssue)
class AssetIssueAdmin(admin.ModelAdmin):
    list_display = ['asset', 'quantity', 'user_type', 'issue_date']
    list_filter = ['created_at', 'user_type', 'issue_date']
    search_fields = ['asset__name', 'issue_to__email']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


