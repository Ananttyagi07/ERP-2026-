"""Superadmin serializers"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import SuperAdminProfile
from apps.roles.models import Role
from apps.users.models import UserRoleAssignment

User = get_user_model()


class SuperAdminListSerializer(serializers.ModelSerializer):
    """List serializer"""
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    user_phone = serializers.CharField(source='user.phone', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)

    class Meta:
        model = SuperAdminProfile
        fields = ['id', 'user_id', 'user_email', 'user_name', 'user_phone', 'photo', 'national_id', 'created_at']


class SuperAdminDetailSerializer(serializers.ModelSerializer):
    """Detail serializer"""
    user = serializers.SerializerMethodField()

    class Meta:
        model = SuperAdminProfile
        fields = '__all__'

    def get_user(self, obj):
        return {
            'id': obj.user.id,
            'email': obj.user.email,
            'username': obj.user.username,
            'first_name': obj.user.first_name,
            'last_name': obj.user.last_name,
            'phone': obj.user.phone,
            'gender': getattr(obj.user, 'gender', ''),
        }


class SuperAdminCreateSerializer(serializers.Serializer):
    """Create serializer"""
    # User fields
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    gender = serializers.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female')], required=True)
    college_id = serializers.IntegerField(required=True)

    # Profile fields
    national_id = serializers.CharField(required=False, allow_blank=True)
    blood_group = serializers.CharField(required=False, allow_blank=True)
    religion = serializers.CharField(required=False, allow_blank=True)
    birth_date = serializers.DateField(required=False, allow_null=True)
    present_address = serializers.CharField(required=False, allow_blank=True)
    permanent_address = serializers.CharField(required=False, allow_blank=True)
    resume = serializers.FileField(required=False, allow_null=True)
    photo = serializers.ImageField(required=False, allow_null=True)
    other_info = serializers.CharField(required=False, allow_blank=True)

    def create(self, validated_data):
        # Extract user fields
        user_data = {
            'email': validated_data.pop('email'),
            'username': validated_data.pop('username'),
            'first_name': validated_data.pop('first_name'),
            'last_name': validated_data.pop('last_name'),
            'phone': validated_data.pop('phone'),
            'college_id': validated_data.pop('college_id'),
        }
        password = validated_data.pop('password')
        gender = validated_data.pop('gender', '')

        # Create user
        user = User.objects.create_user(**user_data, password=password)
        if gender:
            user.gender = gender
            user.save()

        # Assign Superadmin role
        try:
            superadmin_role = Role.objects.get(name='Superadmin')
            UserRoleAssignment.objects.create(
                user=user,
                role=superadmin_role,
                college=user.college,
                is_active=True
            )
        except Role.DoesNotExist:
            pass

        # Create profile
        profile = SuperAdminProfile.objects.create(user=user, college=user.college, **validated_data)
        return profile
