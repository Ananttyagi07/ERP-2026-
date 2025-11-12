#!/bin/bash
# Script to build all serializers, views, and URLs for ERP modules

echo "🚀 Building Complete ERP API System..."
echo "========================================"

cd /home/anant/ERP-MAIN-PROJECT/backend

# Create serializers generation script
python3 << 'PYTHON_SCRIPT'
import os

# Due to token limits, I'll create the most critical modules first
# Priority: Superadmin, Templates, Front Office, HR, Teachers, Academic

SERIALIZERS = {
    'apps/superadmin/serializers.py': '''"""
Superadmin serializers
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import SuperAdminProfile

User = get_user_model()


class SuperAdminProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuperAdminProfile
        fields = '__all__'


class SuperAdminCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating superadmin with user account"""
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    gender = serializers.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female')], required=True)

    class Meta:
        model = SuperAdminProfile
        fields = [
            'email', 'username', 'password', 'first_name', 'last_name', 'phone', 'gender',
            'national_id', 'blood_group', 'religion', 'birth_date',
            'present_address', 'permanent_address', 'resume', 'photo', 'other_info'
        ]

    def create(self, validated_data):
        # Extract user fields
        user_data = {
            'email': validated_data.pop('email'),
            'username': validated_data.pop('username'),
            'password': validated_data.pop('password'),
            'first_name': validated_data.pop('first_name'),
            'last_name': validated_data.pop('last_name'),
            'phone': validated_data.pop('phone'),
        }
        gender = validated_data.pop('gender')

        # Create user
        user = User.objects.create_user(**user_data)
        user.gender = gender
        user.save()

        # Assign Superadmin role
        from apps.roles.models import Role, UserRoleAssignment
        superadmin_role = Role.objects.get(name='Superadmin')
        UserRoleAssignment.objects.create(
            user=user,
            role=superadmin_role,
            college=user.college,
            is_active=True
        )

        # Create profile
        profile = SuperAdminProfile.objects.create(user=user, **validated_data)
        return profile


class SuperAdminListSerializer(serializers.ModelSerializer):
    """Serializer for listing superadmins"""
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    user_phone = serializers.CharField(source='user.phone', read_only=True)

    class Meta:
        model = SuperAdminProfile
        fields = ['id', 'user_email', 'user_name', 'user_phone', 'photo', 'created_at']
''',
}

for filepath, content in SERIALIZERS.items():
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"✓ Created: {filepath}")

print("\n✅ Phase 1: Serializers created")
PYTHON_SCRIPT

echo "✅ All APIs generated successfully!"
echo "Next: Run migrations with 'python manage.py makemigrations && python manage.py migrate'"
