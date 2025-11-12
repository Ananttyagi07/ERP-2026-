"""
Serializers for miscellaneous
"""
from rest_framework import serializers
from .models import Award, Todo, FAQ


class AwardListSerializer(serializers.ModelSerializer):
    """List serializer for Award"""

    class Meta:
        model = Award
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class AwardCreateSerializer(serializers.ModelSerializer):
    """Create/Update serializer for Award"""

    class Meta:
        model = Award
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class AwardDetailSerializer(serializers.ModelSerializer):
    """Detail serializer for Award"""

    class Meta:
        model = Award
        fields = '__all__'
        depth = 1


class TodoListSerializer(serializers.ModelSerializer):
    """List serializer for Todo"""

    class Meta:
        model = Todo
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class TodoCreateSerializer(serializers.ModelSerializer):
    """Create/Update serializer for Todo"""

    class Meta:
        model = Todo
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class TodoDetailSerializer(serializers.ModelSerializer):
    """Detail serializer for Todo"""

    class Meta:
        model = Todo
        fields = '__all__'
        depth = 1


class FAQListSerializer(serializers.ModelSerializer):
    """List serializer for FAQ"""

    class Meta:
        model = FAQ
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class FAQCreateSerializer(serializers.ModelSerializer):
    """Create/Update serializer for FAQ"""

    class Meta:
        model = FAQ
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class FAQDetailSerializer(serializers.ModelSerializer):
    """Detail serializer for FAQ"""

    class Meta:
        model = FAQ
        fields = '__all__'
        depth = 1


