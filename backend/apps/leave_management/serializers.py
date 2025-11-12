"""Leave Management serializers"""
from rest_framework import serializers
from .models import LeaveType, LeaveApplication


class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = '__all__'


class LeaveApplicationSerializer(serializers.ModelSerializer):
    applicant_name = serializers.CharField(source='applicant.get_full_name', read_only=True)
    leave_type_name = serializers.CharField(source='leave_type.name', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.get_full_name', read_only=True, allow_null=True)
    total_days = serializers.ReadOnlyField()

    class Meta:
        model = LeaveApplication
        fields = '__all__'
