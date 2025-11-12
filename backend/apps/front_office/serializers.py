"""Front Office serializers"""
from rest_framework import serializers
from .models import VisitorPurpose, VisitorInfo, CallLog, PostalDispatch, PostalReceive


class VisitorPurposeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitorPurpose
        fields = '__all__'


class VisitorInfoSerializer(serializers.ModelSerializer):
    purpose_name = serializers.CharField(source='purpose.purpose', read_only=True)
    meet_staff_name = serializers.CharField(source='meet_staff_id.get_full_name', read_only=True, allow_null=True)

    class Meta:
        model = VisitorInfo
        fields = '__all__'


class CallLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallLog
        fields = '__all__'


class PostalDispatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostalDispatch
        fields = '__all__'


class PostalReceiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostalReceive
        fields = '__all__'
