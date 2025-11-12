"""HR serializers"""
from rest_framework import serializers
from .models import Designation, Employee


class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = '__all__'


class EmployeeListSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    designation_name = serializers.CharField(source='designation.name', read_only=True)

    class Meta:
        model = Employee
        fields = ['id', 'user_name', 'designation_name', 'joining_date', 'photo']


class EmployeeDetailSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    designation_name = serializers.CharField(source='designation.name', read_only=True)

    class Meta:
        model = Employee
        fields = '__all__'

    def get_user(self, obj):
        return {
            'id': obj.user.id,
            'email': obj.user.email,
            'username': obj.user.username,
            'full_name': obj.user.get_full_name(),
            'phone': obj.user.phone,
        }
