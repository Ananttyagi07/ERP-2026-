"""
Role and Permission models for RBAC system
"""
from django.db import models
from apps.core.models import TimeStampedModel


class Permission(TimeStampedModel):
    """
    Granular permissions for specific actions
    Example: 'view_attendance', 'create_course', 'delete_user'
    """
    name = models.CharField(max_length=100, unique=True, db_index=True)
    codename = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    module = models.CharField(max_length=100, db_index=True, help_text="Module name: attendance, courses, finance, etc.")

    class Meta:
        db_table = 'permissions'
        ordering = ['module', 'name']
        verbose_name = 'Permission'
        verbose_name_plural = 'Permissions'

    def __str__(self):
        return f"{self.module}.{self.codename}"


class Role(TimeStampedModel):
    """
    User roles with dynamic permissions
    Supports both default system roles and custom roles created by Superadmin
    """
    name = models.CharField(max_length=100, unique=True, db_index=True)
    description = models.TextField(blank=True)
    is_default = models.BooleanField(
        default=False,
        help_text="System default roles (Superadmin, Admin, Teacher, Student, Staff)"
    )
    is_system_role = models.BooleanField(
        default=False,
        help_text="Protected system roles that cannot be deleted"
    )

    # Optional college-specific role
    college = models.ForeignKey(
        'colleges.College',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='custom_roles',
        help_text="If set, this role is specific to a college"
    )

    # Creator of this role (for custom roles)
    created_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_roles'
    )

    # Permissions assigned to this role
    permissions = models.ManyToManyField(
        Permission,
        through='RolePermission',
        related_name='roles'
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'user_roles'
        ordering = ['name']
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.name


class RolePermission(TimeStampedModel):
    """
    Junction table for Role-Permission relationship
    Allows tracking when permissions were assigned to roles
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

    # Optional college-specific permission assignment
    college = models.ForeignKey(
        'colleges.College',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    assigned_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='permission_assignments'
    )

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
