"""
Serializers for Role and Permission management
"""
from rest_framework import serializers
from .models import Role, Permission, RolePermission


class PermissionSerializer(serializers.ModelSerializer):
    """Serializer for Permission model"""
    codename = serializers.CharField(source='name', read_only=True)

    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename', 'description', 'module', 'created_at']
        read_only_fields = ['created_at']


class PermissionGroupedSerializer(serializers.Serializer):
    """
    Serializer for permissions grouped by module
    Used in permission assignment UI
    """
    module = serializers.CharField()
    module_name = serializers.CharField()
    permissions = PermissionSerializer(many=True)


class RoleListSerializer(serializers.ModelSerializer):
    """Serializer for Role list view"""
    permissions_count = serializers.SerializerMethodField()
    users_count = serializers.SerializerMethodField()
    college_name = serializers.CharField(source='college.name', read_only=True, allow_null=True)

    class Meta:
        model = Role
        fields = [
            'id', 'name', 'description', 'is_default',
            'college_id', 'college_name',
            'permissions_count', 'users_count', 'created_at'
        ]
        read_only_fields = ['created_at']

    def get_permissions_count(self, obj):
        """Get count of permissions assigned to this role"""
        return obj.permissions.count()

    def get_users_count(self, obj):
        """Get count of users with this role"""
        return obj.user_assignments.filter(is_active=True).count()


class RoleCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating roles"""
    college_id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = Role
        fields = [
            'id', 'name', 'description', 'college_id', 'is_default'
        ]
        read_only_fields = ['id']

    def validate_name(self, value):
        """Validate role name is unique"""
        role_id = self.instance.id if self.instance else None
        if Role.objects.filter(name=value).exclude(id=role_id).exists():
            raise serializers.ValidationError('A role with this name already exists')
        return value

    def create(self, validated_data):
        """Create role with college if college_id is provided"""
        college_id = validated_data.pop('college_id', None)

        role = Role.objects.create(**validated_data)

        # Set college if college_id was provided
        if college_id:
            from apps.colleges.models import College
            try:
                college = College.objects.get(id=college_id)
                role.college = college
                role.save()
            except College.DoesNotExist:
                pass

        return role


class RoleDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for Role with permissions"""
    permissions = PermissionSerializer(many=True, read_only=True)
    college_name = serializers.CharField(source='college.name', read_only=True, allow_null=True)
    users_count = serializers.SerializerMethodField()

    class Meta:
        model = Role
        fields = [
            'id', 'name', 'description', 'is_default',
            'college_id', 'college_name',
            'users_count', 'permissions', 'created_at'
        ]
        read_only_fields = ['created_at']

    def get_users_count(self, obj):
        """Get count of users with this role"""
        return obj.user_assignments.filter(is_active=True).count()


class RolePermissionAssignSerializer(serializers.Serializer):
    """
    Serializer for assigning permissions to a role
    Accepts a list of permission IDs
    """
    permission_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=True,
        allow_empty=False
    )

    def validate_permission_ids(self, value):
        """Validate that all permission IDs exist"""
        existing_ids = Permission.objects.filter(id__in=value).values_list('id', flat=True)
        invalid_ids = set(value) - set(existing_ids)

        if invalid_ids:
            raise serializers.ValidationError(
                f'Invalid permission IDs: {", ".join(map(str, invalid_ids))}'
            )

        return value


class RolePermissionBulkAssignSerializer(serializers.Serializer):
    """
    Serializer for bulk permission assignment with module-level control
    Format: {module: [permission_ids]}
    """
    permissions = serializers.DictField(
        child=serializers.ListField(child=serializers.IntegerField()),
        required=True
    )


class PermissionCheckboxSerializer(serializers.Serializer):
    """
    Serializer for permission checkbox interface
    Returns permissions with their current assignment status
    """
    permission_id = serializers.IntegerField()
    name = serializers.CharField()
    codename = serializers.CharField()
    module = serializers.CharField()
    action = serializers.CharField()
    is_assigned = serializers.BooleanField()
