"""
Custom DRF permissions for Role management
"""
from rest_framework.permissions import BasePermission


class IsSuperadminOrAdmin(BasePermission):
    """
    Only Superadmin or Admin roles can manage roles and permissions
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        # Superuser always has permission
        if request.user.is_superuser:
            return True

        # Check if user has Admin or Superadmin role
        primary_role = request.user.get_primary_role()
        if primary_role and primary_role.name in ['Superadmin', 'Admin']:
            return True

        # Check if user has the specific permission
        if view.action == 'list' or view.action == 'retrieve':
            return request.user.has_permission('view_role')
        elif view.action == 'create':
            return request.user.has_permission('create_role')
        elif view.action in ['update', 'partial_update']:
            return request.user.has_permission('edit_role')
        elif view.action == 'destroy':
            return request.user.has_permission('edit_role')

        return False


class CanManagePermissions(BasePermission):
    """
    Check if user can manage permissions (view_role_permission, edit_role_permission)
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return request.user.has_permission('view_role_permission')

        return request.user.has_permission('edit_role_permission')
