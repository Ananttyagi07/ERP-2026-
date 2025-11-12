"""
Inventory Management models
"""
from django.db import models
from apps.core.models import TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel


class Supplier(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Product suppliers"""
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    address = models.TextField()

    class Meta:
        db_table = 'suppliers'

    def __str__(self):
        return self.name


class Warehouse(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Storage warehouses"""
    title = models.CharField(max_length=255)
    address = models.TextField()

    class Meta:
        db_table = 'warehouses'

    def __str__(self):
        return self.title


class InventoryCategory(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Product categories"""
    name = models.CharField(max_length=255)
    note = models.TextField(blank=True)

    class Meta:
        db_table = 'inventory_categories'
        unique_together = [['college', 'name']]

    def __str__(self):
        return self.name


class Product(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Products/Items"""
    name = models.CharField(max_length=255)
    category = models.ForeignKey(InventoryCategory, on_delete=models.CASCADE, related_name='products')
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    unit = models.CharField(max_length=50, help_text="e.g., Piece, Box, Kg")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'products'

    def __str__(self):
        return f"{self.name} ({self.quantity} {self.unit})"


class Purchase(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Purchase records"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='purchases')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    purchase_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    purchased_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'purchases'

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Purchase: {self.product.name} - {self.quantity} units"


class Sale(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Sales records"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sales')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    sale_date = models.DateField()
    customer_name = models.CharField(max_length=255)
    customer_phone = models.CharField(max_length=20, blank=True)
    invoice_no = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    sold_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'sales'

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Sale: {self.product.name} - Invoice: {self.invoice_no}"


class ProductIssue(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Product issue/return tracking"""
    ISSUE_TYPES = [
        ('Issue', 'Issue'),
        ('Return', 'Return'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='issues')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    issue_type = models.CharField(max_length=10, choices=ISSUE_TYPES)
    quantity = models.IntegerField()
    issue_to = models.CharField(max_length=255, help_text="Department, Person, or Class")
    issue_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    note = models.TextField(blank=True)
    issued_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'product_issues'

    def __str__(self):
        return f"{self.issue_type}: {self.product.name} - {self.quantity} units"
