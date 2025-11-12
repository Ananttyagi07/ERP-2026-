from django.contrib import admin
from .models import Supplier, Warehouse, InventoryCategory, Product, Purchase, Sale, ProductIssue

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email']
    search_fields = ['name', 'phone', 'email']

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ['title', 'address']
    search_fields = ['title']

@admin.register(InventoryCategory)
class InventoryCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'college']
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'warehouse', 'unit_price', 'quantity']
    search_fields = ['name']
    list_filter = ['category', 'warehouse']

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['product', 'supplier', 'quantity', 'total_price', 'purchase_date']
    search_fields = ['product__name']
    list_filter = ['purchase_date', 'supplier']

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['product', 'customer_name', 'quantity', 'total_price', 'invoice_no', 'sale_date']
    search_fields = ['product__name', 'customer_name', 'invoice_no']
    list_filter = ['sale_date']

@admin.register(ProductIssue)
class ProductIssueAdmin(admin.ModelAdmin):
    list_display = ['product', 'issue_type', 'quantity', 'issue_to', 'issue_date']
    search_fields = ['product__name', 'issue_to']
    list_filter = ['issue_type', 'issue_date']
