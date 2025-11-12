"""
Serializers for library
"""
from rest_framework import serializers
from .models import Book, LibraryMember, BookIssue, EBook


class BookListSerializer(serializers.ModelSerializer):
    """List serializer for Book"""

    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class BookCreateSerializer(serializers.ModelSerializer):
    """Create/Update serializer for Book"""

    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class BookDetailSerializer(serializers.ModelSerializer):
    """Detail serializer for Book"""

    class Meta:
        model = Book
        fields = '__all__'
        depth = 1


class LibraryMemberListSerializer(serializers.ModelSerializer):
    """List serializer for LibraryMember"""

    class Meta:
        model = LibraryMember
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class LibraryMemberCreateSerializer(serializers.ModelSerializer):
    """Create/Update serializer for LibraryMember"""

    class Meta:
        model = LibraryMember
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class LibraryMemberDetailSerializer(serializers.ModelSerializer):
    """Detail serializer for LibraryMember"""

    class Meta:
        model = LibraryMember
        fields = '__all__'
        depth = 1


class BookIssueListSerializer(serializers.ModelSerializer):
    """List serializer for BookIssue"""

    class Meta:
        model = BookIssue
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class BookIssueCreateSerializer(serializers.ModelSerializer):
    """Create/Update serializer for BookIssue"""

    class Meta:
        model = BookIssue
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class BookIssueDetailSerializer(serializers.ModelSerializer):
    """Detail serializer for BookIssue"""

    class Meta:
        model = BookIssue
        fields = '__all__'
        depth = 1


class EBookListSerializer(serializers.ModelSerializer):
    """List serializer for EBook"""

    class Meta:
        model = EBook
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class EBookCreateSerializer(serializers.ModelSerializer):
    """Create/Update serializer for EBook"""

    class Meta:
        model = EBook
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class EBookDetailSerializer(serializers.ModelSerializer):
    """Detail serializer for EBook"""

    class Meta:
        model = EBook
        fields = '__all__'
        depth = 1


