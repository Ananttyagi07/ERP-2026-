"""
Serializers for transport
"""
from rest_framework import serializers
from .models import Vehicle, TransportRoute, RouteStop, TransportMember


class VehicleListSerializer(serializers.ModelSerializer):
    """List serializer for Vehicle"""

    class Meta:
        model = Vehicle
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class VehicleCreateSerializer(serializers.ModelSerializer):
    """Create/Update serializer for Vehicle"""

    class Meta:
        model = Vehicle
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class VehicleDetailSerializer(serializers.ModelSerializer):
    """Detail serializer for Vehicle"""

    class Meta:
        model = Vehicle
        fields = '__all__'
        depth = 1


class TransportRouteListSerializer(serializers.ModelSerializer):
    """List serializer for TransportRoute"""

    class Meta:
        model = TransportRoute
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class TransportRouteCreateSerializer(serializers.ModelSerializer):
    """Create/Update serializer for TransportRoute"""

    class Meta:
        model = TransportRoute
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class TransportRouteDetailSerializer(serializers.ModelSerializer):
    """Detail serializer for TransportRoute"""

    class Meta:
        model = TransportRoute
        fields = '__all__'
        depth = 1


class RouteStopListSerializer(serializers.ModelSerializer):
    """List serializer for RouteStop"""

    class Meta:
        model = RouteStop
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class RouteStopCreateSerializer(serializers.ModelSerializer):
    """Create/Update serializer for RouteStop"""

    class Meta:
        model = RouteStop
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class RouteStopDetailSerializer(serializers.ModelSerializer):
    """Detail serializer for RouteStop"""

    class Meta:
        model = RouteStop
        fields = '__all__'
        depth = 1


class TransportMemberListSerializer(serializers.ModelSerializer):
    """List serializer for TransportMember"""

    class Meta:
        model = TransportMember
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class TransportMemberCreateSerializer(serializers.ModelSerializer):
    """Create/Update serializer for TransportMember"""

    class Meta:
        model = TransportMember
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class TransportMemberDetailSerializer(serializers.ModelSerializer):
    """Detail serializer for TransportMember"""

    class Meta:
        model = TransportMember
        fields = '__all__'
        depth = 1


