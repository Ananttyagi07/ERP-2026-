"""
Serializers for payroll
"""
from rest_framework import serializers
from .models import SalaryGrade, SalaryPayment


class SalaryGradeListSerializer(serializers.ModelSerializer):
    """List serializer for SalaryGrade"""

    class Meta:
        model = SalaryGrade
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class SalaryGradeCreateSerializer(serializers.ModelSerializer):
    """Create/Update serializer for SalaryGrade"""

    class Meta:
        model = SalaryGrade
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class SalaryGradeDetailSerializer(serializers.ModelSerializer):
    """Detail serializer for SalaryGrade"""

    class Meta:
        model = SalaryGrade
        fields = '__all__'
        depth = 1


class SalaryPaymentListSerializer(serializers.ModelSerializer):
    """List serializer for SalaryPayment"""

    class Meta:
        model = SalaryPayment
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class SalaryPaymentCreateSerializer(serializers.ModelSerializer):
    """Create/Update serializer for SalaryPayment"""

    class Meta:
        model = SalaryPayment
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class SalaryPaymentDetailSerializer(serializers.ModelSerializer):
    """Detail serializer for SalaryPayment"""

    class Meta:
        model = SalaryPayment
        fields = '__all__'
        depth = 1


