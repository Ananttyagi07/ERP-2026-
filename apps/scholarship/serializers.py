"""
Serializers for scholarship
"""
from rest_framework import serializers
from .models import ScholarshipCandidate, Donor, Scholarship


class ScholarshipCandidateListSerializer(serializers.ModelSerializer):
    """List serializer for ScholarshipCandidate"""

    class Meta:
        model = ScholarshipCandidate
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class ScholarshipCandidateCreateSerializer(serializers.ModelSerializer):
    """Create/Update serializer for ScholarshipCandidate"""

    class Meta:
        model = ScholarshipCandidate
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class ScholarshipCandidateDetailSerializer(serializers.ModelSerializer):
    """Detail serializer for ScholarshipCandidate"""

    class Meta:
        model = ScholarshipCandidate
        fields = '__all__'
        depth = 1


class DonorListSerializer(serializers.ModelSerializer):
    """List serializer for Donor"""

    class Meta:
        model = Donor
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class DonorCreateSerializer(serializers.ModelSerializer):
    """Create/Update serializer for Donor"""

    class Meta:
        model = Donor
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class DonorDetailSerializer(serializers.ModelSerializer):
    """Detail serializer for Donor"""

    class Meta:
        model = Donor
        fields = '__all__'
        depth = 1


class ScholarshipListSerializer(serializers.ModelSerializer):
    """List serializer for Scholarship"""

    class Meta:
        model = Scholarship
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class ScholarshipCreateSerializer(serializers.ModelSerializer):
    """Create/Update serializer for Scholarship"""

    class Meta:
        model = Scholarship
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class ScholarshipDetailSerializer(serializers.ModelSerializer):
    """Detail serializer for Scholarship"""

    class Meta:
        model = Scholarship
        fields = '__all__'
        depth = 1


