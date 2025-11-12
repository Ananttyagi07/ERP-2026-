"""
Serializers for asset_management
"""
from rest_framework import serializers
from .models import Vendor, Store, AssetCategory, AssetItem, AssetPurchase, AssetIssue


class VendorListSerializer(serializers.ModelSerializer):
    """List serializer for Vendor"""

    class Meta:
        model = Vendor
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class VendorCreateSerializer(serializers.ModelSerializer):
    """Create/Update serializer for Vendor"""

    class Meta:
        model = Vendor
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class VendorDetailSerializer(serializers.ModelSerializer):
    """Detail serializer for Vendor"""

    class Meta:
        model = Vendor
        fields = '__all__'
        depth = 1


class StoreListSerializer(serializers.ModelSerializer):
    """List serializer for Store"""

    class Meta:
        model = Store
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class StoreCreateSerializer(serializers.ModelSerializer):
    """Create/Update serializer for Store"""

    class Meta:
        model = Store
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class StoreDetailSerializer(serializers.ModelSerializer):
    """Detail serializer for Store"""

    class Meta:
        model = Store
        fields = '__all__'
        depth = 1


class AssetCategoryListSerializer(serializers.ModelSerializer):
    """List serializer for AssetCategory"""

    class Meta:
        model = AssetCategory
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class AssetCategoryCreateSerializer(serializers.ModelSerializer):
    """Create/Update serializer for AssetCategory"""

    class Meta:
        model = AssetCategory
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class AssetCategoryDetailSerializer(serializers.ModelSerializer):
    """Detail serializer for AssetCategory"""

    class Meta:
        model = AssetCategory
        fields = '__all__'
        depth = 1


class AssetItemListSerializer(serializers.ModelSerializer):
    """List serializer for AssetItem"""

    class Meta:
        model = AssetItem
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class AssetItemCreateSerializer(serializers.ModelSerializer):
    """Create/Update serializer for AssetItem"""

    class Meta:
        model = AssetItem
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class AssetItemDetailSerializer(serializers.ModelSerializer):
    """Detail serializer for AssetItem"""

    class Meta:
        model = AssetItem
        fields = '__all__'
        depth = 1


class AssetPurchaseListSerializer(serializers.ModelSerializer):
    """List serializer for AssetPurchase"""

    class Meta:
        model = AssetPurchase
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class AssetPurchaseCreateSerializer(serializers.ModelSerializer):
    """Create/Update serializer for AssetPurchase"""

    class Meta:
        model = AssetPurchase
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class AssetPurchaseDetailSerializer(serializers.ModelSerializer):
    """Detail serializer for AssetPurchase"""

    class Meta:
        model = AssetPurchase
        fields = '__all__'
        depth = 1


class AssetIssueListSerializer(serializers.ModelSerializer):
    """List serializer for AssetIssue"""

    class Meta:
        model = AssetIssue
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class AssetIssueCreateSerializer(serializers.ModelSerializer):
    """Create/Update serializer for AssetIssue"""

    class Meta:
        model = AssetIssue
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class AssetIssueDetailSerializer(serializers.ModelSerializer):
    """Detail serializer for AssetIssue"""

    class Meta:
        model = AssetIssue
        fields = '__all__'
        depth = 1


