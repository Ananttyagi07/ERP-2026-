"""
Serializers for announcement
"""
from rest_framework import serializers
from .models import Notice, News, Holiday


class NoticeListSerializer(serializers.ModelSerializer):
    """List serializer for Notice"""

    class Meta:
        model = Notice
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class NoticeCreateSerializer(serializers.ModelSerializer):
    """Create/Update serializer for Notice"""

    class Meta:
        model = Notice
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class NoticeDetailSerializer(serializers.ModelSerializer):
    """Detail serializer for Notice"""

    class Meta:
        model = Notice
        fields = '__all__'
        depth = 1


class NewsListSerializer(serializers.ModelSerializer):
    """List serializer for News"""

    class Meta:
        model = News
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class NewsCreateSerializer(serializers.ModelSerializer):
    """Create/Update serializer for News"""

    class Meta:
        model = News
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class NewsDetailSerializer(serializers.ModelSerializer):
    """Detail serializer for News"""

    class Meta:
        model = News
        fields = '__all__'
        depth = 1


class HolidayListSerializer(serializers.ModelSerializer):
    """List serializer for Holiday"""

    class Meta:
        model = Holiday
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class HolidayCreateSerializer(serializers.ModelSerializer):
    """Create/Update serializer for Holiday"""

    class Meta:
        model = Holiday
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class HolidayDetailSerializer(serializers.ModelSerializer):
    """Detail serializer for Holiday"""

    class Meta:
        model = Holiday
        fields = '__all__'
        depth = 1


