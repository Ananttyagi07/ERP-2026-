"""
Serializers for accounting
"""
from rest_framework import serializers
from .models import Discount, FeeType, Invoice, Payment, IncomeHead, Income, ExpenditureHead, Expenditure


class DiscountListSerializer(serializers.ModelSerializer):
    """List serializer for Discount"""

    class Meta:
        model = Discount
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class DiscountCreateSerializer(serializers.ModelSerializer):
    """Create/Update serializer for Discount"""

    class Meta:
        model = Discount
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class DiscountDetailSerializer(serializers.ModelSerializer):
    """Detail serializer for Discount"""

    class Meta:
        model = Discount
        fields = '__all__'
        depth = 1


class FeeTypeListSerializer(serializers.ModelSerializer):
    """List serializer for FeeType"""

    class Meta:
        model = FeeType
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class FeeTypeCreateSerializer(serializers.ModelSerializer):
    """Create/Update serializer for FeeType"""

    class Meta:
        model = FeeType
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class FeeTypeDetailSerializer(serializers.ModelSerializer):
    """Detail serializer for FeeType"""

    class Meta:
        model = FeeType
        fields = '__all__'
        depth = 1


class InvoiceListSerializer(serializers.ModelSerializer):
    """List serializer for Invoice"""

    class Meta:
        model = Invoice
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class InvoiceCreateSerializer(serializers.ModelSerializer):
    """Create/Update serializer for Invoice"""

    class Meta:
        model = Invoice
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class InvoiceDetailSerializer(serializers.ModelSerializer):
    """Detail serializer for Invoice"""

    class Meta:
        model = Invoice
        fields = '__all__'
        depth = 1


class PaymentListSerializer(serializers.ModelSerializer):
    """List serializer for Payment"""

    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class PaymentCreateSerializer(serializers.ModelSerializer):
    """Create/Update serializer for Payment"""

    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class PaymentDetailSerializer(serializers.ModelSerializer):
    """Detail serializer for Payment"""

    class Meta:
        model = Payment
        fields = '__all__'
        depth = 1


class IncomeHeadListSerializer(serializers.ModelSerializer):
    """List serializer for IncomeHead"""

    class Meta:
        model = IncomeHead
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class IncomeHeadCreateSerializer(serializers.ModelSerializer):
    """Create/Update serializer for IncomeHead"""

    class Meta:
        model = IncomeHead
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class IncomeHeadDetailSerializer(serializers.ModelSerializer):
    """Detail serializer for IncomeHead"""

    class Meta:
        model = IncomeHead
        fields = '__all__'
        depth = 1


class IncomeListSerializer(serializers.ModelSerializer):
    """List serializer for Income"""

    class Meta:
        model = Income
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class IncomeCreateSerializer(serializers.ModelSerializer):
    """Create/Update serializer for Income"""

    class Meta:
        model = Income
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class IncomeDetailSerializer(serializers.ModelSerializer):
    """Detail serializer for Income"""

    class Meta:
        model = Income
        fields = '__all__'
        depth = 1


class ExpenditureHeadListSerializer(serializers.ModelSerializer):
    """List serializer for ExpenditureHead"""

    class Meta:
        model = ExpenditureHead
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class ExpenditureHeadCreateSerializer(serializers.ModelSerializer):
    """Create/Update serializer for ExpenditureHead"""

    class Meta:
        model = ExpenditureHead
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class ExpenditureHeadDetailSerializer(serializers.ModelSerializer):
    """Detail serializer for ExpenditureHead"""

    class Meta:
        model = ExpenditureHead
        fields = '__all__'
        depth = 1


class ExpenditureListSerializer(serializers.ModelSerializer):
    """List serializer for Expenditure"""

    class Meta:
        model = Expenditure
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class ExpenditureCreateSerializer(serializers.ModelSerializer):
    """Create/Update serializer for Expenditure"""

    class Meta:
        model = Expenditure
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class ExpenditureDetailSerializer(serializers.ModelSerializer):
    """Detail serializer for Expenditure"""

    class Meta:
        model = Expenditure
        fields = '__all__'
        depth = 1


