"""
Inventory Management serializers
"""
from rest_framework import serializers
from .models import Supplier, Warehouse, InventoryCategory, Product, Purchase, Sale, ProductIssue


class SupplierListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name', 'phone', 'email']


class SupplierCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['name', 'phone', 'email', 'address']


class SupplierDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'


class WarehouseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ['id', 'title', 'address']


class WarehouseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ['title', 'address']


class WarehouseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'


class InventoryCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryCategory
        fields = ['id', 'name', 'note']


class InventoryCategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryCategory
        fields = ['name', 'note']


class InventoryCategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryCategory
        fields = '__all__'


class ProductListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    warehouse_title = serializers.CharField(source='warehouse.title', read_only=True)
    supplier_name = serializers.CharField(source='supplier.name', read_only=True, allow_null=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'category_name', 'warehouse_title', 'supplier_name',
            'unit', 'unit_price', 'quantity'
        ]


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'name', 'category', 'supplier', 'warehouse',
            'unit', 'unit_price', 'quantity', 'description'
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    warehouse_title = serializers.CharField(source='warehouse.title', read_only=True)
    supplier_name = serializers.CharField(source='supplier.name', read_only=True, allow_null=True)

    class Meta:
        model = Product
        fields = '__all__'


class PurchaseListSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)

    class Meta:
        model = Purchase
        fields = [
            'id', 'product_name', 'supplier_name', 'quantity',
            'unit_price', 'total_price', 'purchase_date'
        ]


class PurchaseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = [
            'product', 'supplier', 'warehouse', 'quantity', 'unit_price',
            'purchase_date', 'expiry_date', 'description'
        ]


class PurchaseDetailSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    warehouse_title = serializers.CharField(source='warehouse.title', read_only=True)
    purchased_by_name = serializers.CharField(source='purchased_by.get_full_name', read_only=True, allow_null=True)

    class Meta:
        model = Purchase
        fields = '__all__'


class SaleListSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = Sale
        fields = [
            'id', 'product_name', 'customer_name', 'quantity',
            'unit_price', 'total_price', 'invoice_no', 'sale_date'
        ]


class SaleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = [
            'product', 'warehouse', 'quantity', 'unit_price', 'sale_date',
            'customer_name', 'customer_phone', 'invoice_no', 'description'
        ]


class SaleDetailSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    warehouse_title = serializers.CharField(source='warehouse.title', read_only=True)
    sold_by_name = serializers.CharField(source='sold_by.get_full_name', read_only=True, allow_null=True)

    class Meta:
        model = Sale
        fields = '__all__'


class ProductIssueListSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    warehouse_title = serializers.CharField(source='warehouse.title', read_only=True)

    class Meta:
        model = ProductIssue
        fields = [
            'id', 'product_name', 'warehouse_title', 'issue_type',
            'quantity', 'issue_to', 'issue_date', 'return_date'
        ]


class ProductIssueCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductIssue
        fields = [
            'product', 'warehouse', 'issue_type', 'quantity',
            'issue_to', 'issue_date', 'return_date', 'note'
        ]


class ProductIssueDetailSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    warehouse_title = serializers.CharField(source='warehouse.title', read_only=True)
    issued_by_name = serializers.CharField(source='issued_by.get_full_name', read_only=True, allow_null=True)

    class Meta:
        model = ProductIssue
        fields = '__all__'
