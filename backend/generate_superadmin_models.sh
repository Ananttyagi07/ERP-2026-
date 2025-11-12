#!/bin/bash
# Generate ALL Superadmin Feature Models

cd /home/anant/ERP-MAIN-PROJECT/backend

echo "🚀 Generating ALL Superadmin Models..."
echo "======================================================================"

# Asset Management Models
cat > apps/asset_management/models.py << 'EOF'
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
EOF

echo "✓ Asset Management models created"

# Library Models
cat > apps/library/models.py << 'EOF'
"""Library Management models"""
from django.db import models
from apps.core.models import TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel


class Book(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Physical books in library"""
    title = models.CharField(max_length=255)
    book_id = models.CharField(max_length=100, unique=True)
    isbn_no = models.CharField(max_length=50, blank=True)
    edition = models.CharField(max_length=100, blank=True)
    author = models.CharField(max_length=255, blank=True)
    language = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity = models.IntegerField(default=1)
    almira_no = models.CharField(max_length=50, blank=True)
    book_cover = models.ImageField(upload_to='library/books/', null=True, blank=True)

    class Meta:
        db_table = 'library_books'

    def __str__(self):
        return f"{self.title} ({self.book_id})"


class LibraryMember(TimeStampedModel, CollegeIsolatedModel):
    """Library membership for students"""
    student = models.OneToOneField('students.Student', on_delete=models.CASCADE, related_name='library_membership')
    library_id = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'library_members'

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.library_id}"


class BookIssue(TimeStampedModel, CollegeIsolatedModel):
    """Book issue/return records"""
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='issues')
    member = models.ForeignKey(LibraryMember, on_delete=models.CASCADE, related_name='book_issues')
    issue_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    fine_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    class Meta:
        db_table = 'book_issues'

    def __str__(self):
        return f"{self.book.title} - {self.member.student.user.get_full_name()}"


class EBook(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Digital books/documents"""
    school_class = models.ForeignKey('academic.SchoolClass', on_delete=models.CASCADE)
    subject = models.ForeignKey('academic.Subject', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    edition = models.CharField(max_length=100, blank=True)
    author = models.CharField(max_length=255, blank=True)
    language = models.CharField(max_length=100, blank=True)
    cover_image = models.ImageField(upload_to='library/ebook_covers/', null=True, blank=True)
    ebook_file = models.FileField(upload_to='library/ebooks/')

    class Meta:
        db_table = 'ebooks'

    def __str__(self):
        return self.name
EOF

echo "✓ Library models created"

# Transport Models
cat > apps/transport/models.py << 'EOF'
"""Transport Management models"""
from django.db import models
from apps.core.models import TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel


class Vehicle(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Transport vehicles"""
    vehicle_number = models.CharField(max_length=100)
    vehicle_model = models.CharField(max_length=255, blank=True)
    driver = models.CharField(max_length=255, blank=True)
    vehicle_license = models.CharField(max_length=100, blank=True)
    vehicle_contact = models.CharField(max_length=20)
    note = models.TextField(blank=True)

    class Meta:
        db_table = 'vehicles'
        unique_together = [['college', 'vehicle_number']]

    def __str__(self):
        return f"{self.vehicle_number} - {self.vehicle_model}"


class TransportRoute(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Transport routes"""
    route_name = models.CharField(max_length=255)
    route_start = models.CharField(max_length=255)
    route_end = models.CharField(max_length=255)
    note = models.TextField(blank=True)

    class Meta:
        db_table = 'transport_routes'

    def __str__(self):
        return self.route_name


class RouteStop(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Stops on transport routes"""
    route = models.ForeignKey(TransportRoute, on_delete=models.CASCADE, related_name='stops')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='assigned_stops')
    stop_name = models.CharField(max_length=255)
    stop_km = models.DecimalField(max_digits=6, decimal_places=2)
    stop_fare = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        db_table = 'route_stops'

    def __str__(self):
        return f"{self.route.route_name} - {self.stop_name}"


class TransportMember(TimeStampedModel, CollegeIsolatedModel):
    """Students using transport"""
    student = models.OneToOneField('students.Student', on_delete=models.CASCADE, related_name='transport_membership')
    route = models.ForeignKey(TransportRoute, on_delete=models.CASCADE, related_name='members')
    stop = models.ForeignKey(RouteStop, on_delete=models.CASCADE, related_name='members')

    class Meta:
        db_table = 'transport_members'

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.route.route_name}"
EOF

echo "✓ Transport models created"

# Continue in next part...
echo ""
echo "======================================================================"
echo "✅ Part 1 Complete: Asset, Library, Transport models created"
echo "======================================================================"
