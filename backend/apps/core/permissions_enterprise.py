"""
Enterprise Permission System
Automatic permission enforcement for all ViewSets
"""
from rest_framework import permissions
from apps.authentication.models_security import SecurityAuditLog


class BaseModelPermission(permissions.BasePermission):
    """
    Base permission class that automatically maps ViewSet actions to permissions

    Usage:
        class StudentViewSet(viewsets.ModelViewSet):
            permission_classes = [IsAuthenticated, BaseModelPermission]
            permission_module = 'student'  # Module name from ACL

    Automatically maps:
        list() -> view_{module}
        retrieve() -> view_{module}
        create() -> add_{module}
        update() -> edit_{module}
        partial_update() -> edit_{module}
        destroy() -> delete_{module}
    """

    # Action to permission mapping
    ACTION_PERMISSION_MAP = {
        'list': 'view',
        'retrieve': 'view',
        'create': 'add',
        'update': 'edit',
        'partial_update': 'edit',
        'destroy': 'delete',
    }

    def has_permission(self, request, view):
        """
        Check if user has permission for the requested action
        """
        # Skip permission check for unauthenticated users (handled by IsAuthenticated)
        if not request.user or not request.user.is_authenticated:
            return False

        # Superuser always has permission
        if request.user.is_superuser:
            return True

        # Get permission module from view
        permission_module = getattr(view, 'permission_module', None)
        if not permission_module:
            # Try to infer from model name
            if hasattr(view, 'queryset') and view.queryset is not None:
                model_name = view.queryset.model.__name__.lower()
                permission_module = model_name
            else:
                # Can't determine permission module, deny access
                self._log_permission_denied(request, view, 'No permission module specified')
                return False

        # Get action
        action = view.action if hasattr(view, 'action') else None
        if not action:
            # For non-ViewSet views, check method
            action = request.method.lower()

        # Map action to permission type
        permission_type = self.ACTION_PERMISSION_MAP.get(action)
        if not permission_type:
            # Custom action, check if view defines permission
            permission_method = f'get_{action}_permission'
            if hasattr(view, permission_method):
                permission_type = getattr(view, permission_method)()
            else:
                # Default to 'view' for GET, 'edit' for others
                permission_type = 'view' if request.method == 'GET' else 'edit'

        # Build permission codename
        permission_codename = f"{permission_type}_{permission_module}"

        # Check permission
        has_perm = request.user.has_permission(permission_codename)

        if not has_perm:
            # Log permission denied
            self._log_permission_denied(
                request, view,
                f"Missing permission: {permission_codename}",
                permission_codename
            )

        return has_perm

    def _log_permission_denied(self, request, view, reason, permission_codename=None):
        """Log permission denied event to audit log"""
        try:
            resource_type = getattr(view, 'permission_module', 'unknown')

            SecurityAuditLog.log(
                'permission_denied',
                request,
                user=request.user if request.user.is_authenticated else None,
                success=False,
                failure_reason=reason,
                resource_type=resource_type,
                action=view.action if hasattr(view, 'action') else request.method,
                metadata={
                    'permission_required': permission_codename,
                    'user_permissions': list(request.user.get_permissions()) if request.user.is_authenticated else [],
                    'view_class': view.__class__.__name__,
                }
            )
        except Exception as e:
            # Don't fail request if logging fails
            print(f"Failed to log permission denied: {e}")


class IsSuperadmin(permissions.BasePermission):
    """
    Allow access only to Superadmin users
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        # Check role
        primary_role = request.user.get_primary_role()
        is_superadmin = primary_role and primary_role.name == 'Superadmin'

        if not is_superadmin:
            SecurityAuditLog.log(
                'permission_denied',
                request,
                user=request.user,
                success=False,
                failure_reason='Requires Superadmin role',
                resource_type='system',
                action='admin_access'
            )

        return is_superadmin


class IsAdmin(permissions.BasePermission):
    """
    Allow access to Superadmin and Admin users
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        primary_role = request.user.get_primary_role()
        is_admin = primary_role and primary_role.name in ['Superadmin', 'Admin']

        if not is_admin:
            SecurityAuditLog.log(
                'permission_denied',
                request,
                user=request.user,
                success=False,
                failure_reason='Requires Admin or Superadmin role',
                resource_type='admin',
                action='admin_access'
            )

        return is_admin


class IsTeacher(permissions.BasePermission):
    """Allow access only to Teacher role"""
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        primary_role = request.user.get_primary_role()
        return primary_role and primary_role.name == 'Teacher'


class IsStudent(permissions.BasePermission):
    """Allow access only to Student role"""
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        primary_role = request.user.get_primary_role()
        return primary_role and primary_role.name == 'Student'


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Allow access if user is owner of object or has admin role
    """
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False

        # Superadmin can access everything
        if request.user.is_superuser:
            return True

        # Check if admin
        primary_role = request.user.get_primary_role()
        if primary_role and primary_role.name in ['Superadmin', 'Admin']:
            return True

        # Check ownership
        # Try common ownership patterns
        if hasattr(obj, 'user') and obj.user == request.user:
            return True
        if hasattr(obj, 'created_by') and obj.created_by == request.user:
            return True
        if hasattr(obj, 'owner') and obj.owner == request.user:
            return True
        if obj == request.user:
            return True

        # Log unauthorized access attempt
        SecurityAuditLog.log(
            'permission_denied',
            request,
            user=request.user,
            success=False,
            failure_reason='Not owner and not admin',
            resource_type=obj.__class__.__name__,
            resource_id=obj.pk,
            action='object_access'
        )

        return False


def require_permission(*permission_codenames):
    """
    Decorator to require specific permissions

    Usage:
        @require_permission('view_student', 'edit_student')
        def my_view(request):
            pass
    """
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user or not request.user.is_authenticated:
                from rest_framework.response import Response
                from rest_framework import status
                return Response(
                    {'error': 'Authentication required'},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # Superuser bypasses permission checks
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            # Check if user has ANY of the required permissions
            has_permission = any(
                request.user.has_permission(perm)
                for perm in permission_codenames
            )

            if not has_permission:
                # Log denied access
                SecurityAuditLog.log(
                    'permission_denied',
                    request,
                    user=request.user,
                    success=False,
                    failure_reason=f"Missing permissions: {', '.join(permission_codenames)}",
                    metadata={'required_permissions': list(permission_codenames)}
                )

                from rest_framework.response import Response
                from rest_framework import status
                return Response(
                    {
                        'error': 'Permission denied',
                        'required_permissions': list(permission_codenames)
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            return view_func(request, *args, **kwargs)

        return wrapper
    return decorator


def require_role(*role_names):
    """
    Decorator to require specific roles

    Usage:
        @require_role('Admin', 'Teacher')
        def my_view(request):
            pass
    """
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user or not request.user.is_authenticated:
                from rest_framework.response import Response
                from rest_framework import status
                return Response(
                    {'error': 'Authentication required'},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # Superuser bypasses role checks
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            # Get user's primary role
            primary_role = request.user.get_primary_role()
            has_role = primary_role and primary_role.name in role_names

            if not has_role:
                # Log denied access
                SecurityAuditLog.log(
                    'permission_denied',
                    request,
                    user=request.user,
                    success=False,
                    failure_reason=f"Missing roles: {', '.join(role_names)}",
                    metadata={'required_roles': list(role_names)}
                )

                from rest_framework.response import Response
                from rest_framework import status
                return Response(
                    {
                        'error': 'Permission denied',
                        'required_roles': list(role_names)
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            return view_func(request, *args, **kwargs)

        return wrapper
    return decorator


class AuditLoggingMixin:
    """
    Mixin to add automatic audit logging to ViewSets

    Usage:
        class StudentViewSet(AuditLoggingMixin, viewsets.ModelViewSet):
            queryset = Student.objects.all()
            audit_resource_type = 'student'
    """

    def perform_create(self, serializer):
        """Log object creation"""
        instance = serializer.save()

        SecurityAuditLog.log(
            'data_created',
            self.request,
            user=self.request.user,
            success=True,
            resource_type=getattr(self, 'audit_resource_type', instance.__class__.__name__),
            resource_id=instance.pk,
            resource_name=str(instance),
            action='create',
            metadata={
                'model': instance.__class__.__name__,
                'data': serializer.data
            }
        )

    def perform_update(self, serializer):
        """Log object update"""
        # Get old data before update
        old_instance = self.get_object()
        old_data = type(serializer)(old_instance).data

        # Perform update
        instance = serializer.save()

        # Get new data
        new_data = serializer.data

        # Calculate changes
        changes = {}
        for key in new_data.keys():
            if old_data.get(key) != new_data.get(key):
                changes[key] = {
                    'old': old_data.get(key),
                    'new': new_data.get(key)
                }

        SecurityAuditLog.log(
            'data_updated',
            self.request,
            user=self.request.user,
            success=True,
            resource_type=getattr(self, 'audit_resource_type', instance.__class__.__name__),
            resource_id=instance.pk,
            resource_name=str(instance),
            action='update',
            changes=changes,
            metadata={
                'model': instance.__class__.__name__,
                'fields_changed': list(changes.keys())
            }
        )

    def perform_destroy(self, instance):
        """Log object deletion"""
        SecurityAuditLog.log(
            'data_deleted',
            self.request,
            user=self.request.user,
            success=True,
            resource_type=getattr(self, 'audit_resource_type', instance.__class__.__name__),
            resource_id=instance.pk,
            resource_name=str(instance),
            action='delete',
            metadata={
                'model': instance.__class__.__name__,
            }
        )

        instance.delete()

    def list(self, request, *args, **kwargs):
        """Log list access"""
        response = super().list(request, *args, **kwargs)

        if response.status_code == 200:
            SecurityAuditLog.log(
                'data_viewed',
                request,
                user=request.user,
                success=True,
                resource_type=getattr(self, 'audit_resource_type', 'unknown'),
                action='list',
                metadata={
                    'count': response.data.get('count', len(response.data)) if isinstance(response.data, dict) else len(response.data),
                }
            )

        return response

    def retrieve(self, request, *args, **kwargs):
        """Log detail access"""
        response = super().retrieve(request, *args, **kwargs)

        if response.status_code == 200:
            instance = self.get_object()
            SecurityAuditLog.log(
                'data_viewed',
                request,
                user=request.user,
                success=True,
                resource_type=getattr(self, 'audit_resource_type', instance.__class__.__name__),
                resource_id=instance.pk,
                resource_name=str(instance),
                action='view',
            )

        return response
