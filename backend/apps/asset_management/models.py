"""Asset Management models"""
from django.db import models
from apps.core.models import TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel


class Vendor(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Asset vendors/suppliers"""
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20)
    contact_name = models.CharField(max_length=255)
    address = models.TextField(blank=True)
    note = models.TextField(blank=True)

    class Meta:
        db_table = 'asset_vendors'

    def __str__(self):
        return self.name


class Store(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Asset storage locations"""
    name = models.CharField(max_length=255)
    store_keeper = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    note = models.TextField(blank=True)

    class Meta:
        db_table = 'asset_stores'

    def __str__(self):
        return self.name


class AssetCategory(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Asset categories"""
    name = models.CharField(max_length=255)
    note = models.TextField(blank=True)

    class Meta:
        db_table = 'asset_categories'
        unique_together = [['college', 'name']]

    def __str__(self):
        return self.name


class AssetItem(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Asset items/inventory"""
    ITEM_TYPES = [
        ('Consumable', 'Consumable'),
        ('Non-Consumable', 'Non-Consumable'),
    ]

    category = models.ForeignKey(AssetCategory, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=255)
    product_code = models.CharField(max_length=100, blank=True)
    item_type = models.CharField(max_length=20, choices=ITEM_TYPES)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='items')
    note = models.TextField(blank=True)

    class Meta:
        db_table = 'asset_items'

    def __str__(self):
        return f"{self.name} ({self.product_code})"


class AssetPurchase(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Asset purchase records"""
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='purchases')
    category = models.ForeignKey(AssetCategory, on_delete=models.CASCADE)
    asset = models.ForeignKey(AssetItem, on_delete=models.CASCADE, related_name='purchases')
    quantity = models.IntegerField()
    unit_type = models.CharField(max_length=50, blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    purchase_date = models.DateField()
    expire_date = models.DateField(null=True, blank=True)
    purchase_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, related_name='asset_purchases')
    note = models.TextField(blank=True)

    class Meta:
        db_table = 'asset_purchases'

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.asset.name} - {self.quantity} units"


class AssetIssue(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Asset issue/checkout records"""
    USER_TYPES = [
        ('Student', 'Student'),
        ('Teacher', 'Teacher'),
        ('Employee', 'Employee'),
    ]

    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    issue_to = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='asset_issues')
    category = models.ForeignKey(AssetCategory, on_delete=models.CASCADE)
    asset = models.ForeignKey(AssetItem, on_delete=models.CASCADE, related_name='issues')
    quantity = models.IntegerField()
    issue_date = models.DateField()
    check_in = models.DateField()
    check_out = models.DateField(null=True, blank=True)
    note = models.TextField(blank=True)

    class Meta:
        db_table = 'asset_issues'

    def __str__(self):
        return f"{self.asset.name} issued to {self.issue_to.get_full_name()}"
