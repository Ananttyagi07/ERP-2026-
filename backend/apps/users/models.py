"""
User models with RBAC integration
"""
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.cache import cache
from apps.core.models import TimeStampedModel


class UserManager(BaseUserManager):
    """
    Custom user manager for email-based authentication
    """
    def create_user(self, email, password=None, **extra_fields):
        """Create and return a regular user"""
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    """
    Custom User model with college isolation and role-based access
    """
    # Authentication fields
    email = models.EmailField(unique=True, db_index=True)
    username = models.CharField(max_length=150, unique=True, db_index=True)

    # Personal information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    # College association
    college = models.ForeignKey(
        'colleges.College',
        on_delete=models.CASCADE,
        related_name='users',
        db_index=True
    )

    # Department association (optional, mainly for teachers/staff)
    department = models.ForeignKey(
        'colleges.Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users'
    )

    # Status flags
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Django admin access
    is_superuser = models.BooleanField(default=False)  # ERP Superadmin

    # Email verification
    email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=100, blank=True)

    # Password reset
    password_reset_token = models.CharField(max_length=100, blank=True)
    password_reset_expires = models.DateTimeField(null=True, blank=True)

    # Last login tracking
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    last_login_user_agent = models.TextField(blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        db_table = 'users'
        ordering = ['-created_at']
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        indexes = [
            models.Index(fields=['email', 'college']),
            models.Index(fields=['college', 'is_active']),
        ]

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"

    def get_full_name(self):
        """Return full name"""
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        """Return first name"""
        return self.first_name

    def get_primary_role(self):
        """Get user's primary role"""
        role_assignment = self.role_assignments.filter(is_active=True).first()
        return role_assignment.role if role_assignment else None

    def get_all_roles(self):
        """Get all active roles for the user"""
        return [assignment.role for assignment in self.role_assignments.filter(is_active=True)]

    def get_permissions(self):
        """
        Get all permissions for the user from all their roles
        Cached for performance
        """
        cache_key = f'user_permissions_{self.id}'
        permissions = cache.get(cache_key)

        if permissions is None:
            from apps.roles.models import Permission
            role_ids = self.role_assignments.filter(is_active=True).values_list('role_id', flat=True)
            permissions = Permission.objects.filter(
                permission_roles__role_id__in=role_ids
            ).distinct().values('id', 'name', 'codename', 'module')

            permissions = list(permissions)
            cache.set(cache_key, permissions, timeout=300)  # Cache for 5 minutes

        return permissions

    def has_permission(self, permission_codename):
        """Check if user has a specific permission"""
        permissions = self.get_permissions()
        return any(p['codename'] == permission_codename for p in permissions)

    def clear_permission_cache(self):
        """Clear cached permissions for this user"""
        cache_key = f'user_permissions_{self.id}'
        cache.delete(cache_key)


class UserRoleAssignment(TimeStampedModel):
    """
    Junction table for User-Role relationship
    Allows users to have multiple roles
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='role_assignments'
    )
    role = models.ForeignKey(
        'roles.Role',
        on_delete=models.CASCADE,
        related_name='user_assignments'
    )

    # College context (must match user's college)
    college = models.ForeignKey(
        'colleges.College',
        on_delete=models.CASCADE,
        related_name='user_role_assignments'
    )

    # Assignment metadata
    assigned_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='role_assignments_made'
    )
    assigned_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'user_role_assignments'
        unique_together = [['user', 'role']]
        verbose_name = 'User Role Assignment'
        verbose_name_plural = 'User Role Assignments'
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['role', 'is_active']),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.role.name}"

    def save(self, *args, **kwargs):
        """Override save to clear user's permission cache"""
        super().save(*args, **kwargs)
        self.user.clear_permission_cache()

    def delete(self, *args, **kwargs):
        """Override delete to clear user's permission cache"""
        user = self.user
        super().delete(*args, **kwargs)
        user.clear_permission_cache()


# NOTE: Student and Teacher models have been moved to dedicated apps
# - Student model: apps/students/models.py
# - Teacher model: apps/teachers/models.py
# This avoids model name conflicts and provides better separation of concerns
