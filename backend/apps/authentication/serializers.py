"""
Authentication serializers
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login - accepts email and password
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        """Validate login credentials"""
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            raise serializers.ValidationError('Email and password are required')

        # Try to get user
        try:
            user = User.objects.select_related('college').get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid credentials')

        # Check if user is active
        if not user.is_active:
            raise serializers.ValidationError('Account is inactive. Please contact administrator.')

        # Verify password
        if not user.check_password(password):
            raise serializers.ValidationError('Invalid credentials')

        data['user'] = user
        return data


class UserInfoSerializer(serializers.ModelSerializer):
    """
    Serializer for user information in login response
    """
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    college_name = serializers.CharField(source='college.name', read_only=True)
    college_code = serializers.CharField(source='college.code', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True, allow_null=True)
    primary_role = serializers.SerializerMethodField()
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name', 'full_name',
            'phone', 'avatar_url', 'college_id', 'college_name', 'college_code',
            'department_id', 'department_name', 'is_superuser', 'is_staff',
            'primary_role', 'email_verified'
        ]

    def get_primary_role(self, obj):
        """Get user's primary role"""
        role = obj.get_primary_role()
        if role:
            return {
                'id': role.id,
                'name': role.name,
                'description': role.description
            }
        return None

    def get_avatar_url(self, obj):
        """Get avatar URL"""
        if obj.avatar:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.avatar.url)
        return None


class PermissionSerializer(serializers.Serializer):
    """Serializer for user permissions"""
    id = serializers.IntegerField()
    name = serializers.CharField()
    codename = serializers.CharField()
    module = serializers.CharField()


class RefreshTokenSerializer(serializers.Serializer):
    """Serializer for token refresh"""
    refresh_token = serializers.CharField(required=True)
