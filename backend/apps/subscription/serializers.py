"""
Serializers for subscription
"""
from rest_framework import serializers
from .models import SubscriptionPlan, Subscription, SubscriptionPayment


class SubscriptionPlanListSerializer(serializers.ModelSerializer):
    """List serializer for SubscriptionPlan"""

    class Meta:
        model = SubscriptionPlan
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class SubscriptionPlanCreateSerializer(serializers.ModelSerializer):
    """Create/Update serializer for SubscriptionPlan"""

    class Meta:
        model = SubscriptionPlan
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class SubscriptionPlanDetailSerializer(serializers.ModelSerializer):
    """Detail serializer for SubscriptionPlan"""

    class Meta:
        model = SubscriptionPlan
        fields = '__all__'
        depth = 1


class SubscriptionListSerializer(serializers.ModelSerializer):
    """List serializer for Subscription"""

    class Meta:
        model = Subscription
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class SubscriptionCreateSerializer(serializers.ModelSerializer):
    """Create/Update serializer for Subscription"""

    class Meta:
        model = Subscription
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class SubscriptionDetailSerializer(serializers.ModelSerializer):
    """Detail serializer for Subscription"""

    class Meta:
        model = Subscription
        fields = '__all__'
        depth = 1


class SubscriptionPaymentListSerializer(serializers.ModelSerializer):
    """List serializer for SubscriptionPayment"""

    class Meta:
        model = SubscriptionPayment
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class SubscriptionPaymentCreateSerializer(serializers.ModelSerializer):
    """Create/Update serializer for SubscriptionPayment"""

    class Meta:
        model = SubscriptionPayment
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class SubscriptionPaymentDetailSerializer(serializers.ModelSerializer):
    """Detail serializer for SubscriptionPayment"""

    class Meta:
        model = SubscriptionPayment
        fields = '__all__'
        depth = 1


