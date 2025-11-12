"""
Card Generation serializers
"""
from rest_framework import serializers
from .models import IDCardSetting, AdmitCardSetting


class IDCardSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = IDCardSetting
        fields = '__all__'


class AdmitCardSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdmitCardSetting
        fields = '__all__'
