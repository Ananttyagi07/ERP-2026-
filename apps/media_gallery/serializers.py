"""
Serializers for media_gallery
"""
from rest_framework import serializers
from .models import Gallery, GalleryImage


class GalleryListSerializer(serializers.ModelSerializer):
    """List serializer for Gallery"""

    class Meta:
        model = Gallery
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class GalleryCreateSerializer(serializers.ModelSerializer):
    """Create/Update serializer for Gallery"""

    class Meta:
        model = Gallery
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class GalleryDetailSerializer(serializers.ModelSerializer):
    """Detail serializer for Gallery"""

    class Meta:
        model = Gallery
        fields = '__all__'
        depth = 1


class GalleryImageListSerializer(serializers.ModelSerializer):
    """List serializer for GalleryImage"""

    class Meta:
        model = GalleryImage
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class GalleryImageCreateSerializer(serializers.ModelSerializer):
    """Create/Update serializer for GalleryImage"""

    class Meta:
        model = GalleryImage
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class GalleryImageDetailSerializer(serializers.ModelSerializer):
    """Detail serializer for GalleryImage"""

    class Meta:
        model = GalleryImage
        fields = '__all__'
        depth = 1


