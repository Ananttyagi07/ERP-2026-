"""Guardian serializers"""
from rest_framework import serializers
from .models import Guardian


class GuardianListSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    user_phone = serializers.CharField(source='user.phone', read_only=True)

    class Meta:
        model = Guardian
        fields = ['id', 'user_name', 'user_email', 'user_phone', 'occupation', 'photo']


class GuardianDetailSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Guardian
        fields = '__all__'

    def get_user(self, obj):
        return {
            'id': obj.user.id,
            'email': obj.user.email,
            'username': obj.user.username,
            'full_name': obj.user.get_full_name(),
            'phone': obj.user.phone,
        }
