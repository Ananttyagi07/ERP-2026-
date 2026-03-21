"""
Role and Permission models for RBAC system
"""
from django.db import models
from apps.core.models import TimeStampedModel


class Permission(models.Model):
    """
    Granular permissions for specific actions
    Example: 'view_attendance', 'create_course', 'delete_user'
    """
    name = models.CharField(max_length=100, unique=True, db_index=True, db_column='name')
    description = models.TextField(blank=True, db_column='description')
    module = models.CharField(max_length=100, db_index=True, help_text="Module name: attendance, courses, finance, etc.", db_column='module')

    # Track when permission was created
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'permissions'
        ordering = ['module', 'name']
        verbose_name = 'Permission'
        verbose_name_plural = 'Permissions'

    @property
    def codename(self):
        """Backward compatibility property"""
        return self.name

    def __str__(self):
        return f"{self.module}.{self.name}"


class Role(models.Model):
    """
    User roles with dynamic permissions
    Supports both default system roles and custom roles created by Superadmin
    Mapped to existing database schema (only has created_at, not updated_at)
    """
    name = models.CharField(max_length=100, unique=True, db_index=True)
    description = models.TextField(blank=True)
    is_default = models.BooleanField(
        default=False,
        help_text="System default roles (Superadmin, Admin, Teacher, Student, Staff)"
    )



    # Track when role was created
    created_at = models.DateTimeField(auto_now_add=True)

    # Permissions assigned to this role
    permissions = models.ManyToManyField(
        Permission,
        through='RolePermission',
        related_name='roles'
    )

    class Meta:
        db_table = 'user_roles'
        ordering = ['name']
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.name


class RolePermission(models.Model):
    """
    Junction table for Role-Permission relationship
    Allows tracking when permissions were assigned to roles
    Mapped to existing database schema (only has role_id, permission_id, created_at)
    """
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name='role_permissions'
    )
    permission = models.ForeignKey(
        Permission,
        on_delete=models.CASCADE,
        related_name='permission_roles'
    )

    # Track when permission was assigned (created_at field exists in database)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'role_permissions'
        unique_together = [['role', 'permission']]
        verbose_name = 'Role Permission'
        verbose_name_plural = 'Role Permissions'
        indexes = [
            models.Index(fields=['role', 'permission']),
        ]

    def __str__(self):
        return f"{self.role.name} - {self.permission.codename}"
