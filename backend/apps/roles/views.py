"""
Role and Permission Management API views
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Q, Prefetch
from django.shortcuts import get_object_or_404

from .models import Role, Permission, RolePermission
from .serializers import (
    RoleListSerializer,
    RoleCreateSerializer,
    RoleDetailSerializer,
    RolePermissionAssignSerializer,
    PermissionSerializer,
    PermissionGroupedSerializer,
    RolePermissionBulkAssignSerializer,
    PermissionCheckboxSerializer
)
from .permissions import IsSuperadminOrAdmin


class RoleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Role CRUD operations

    GET /api/roles/
    - List all roles with counts
    - Filter: ?is_default=true&is_active=true&college_id=1

    POST /api/roles/
    - Create new custom role

    GET /api/roles/{id}/
    - Get role details with permissions

    PUT /api/roles/{id}/
    - Update role

    PATCH /api/roles/{id}/
    - Partial update role

    DELETE /api/roles/{id}/
    - Delete role (only custom roles, not system roles)
    """
    permission_classes = [IsAuthenticated, IsSuperadminOrAdmin]
    queryset = Role.objects.all()

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return RoleListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return RoleCreateSerializer
        return RoleDetailSerializer

    def get_queryset(self):
        """Filter roles with optional parameters

        Returns:
        - If college_id provided: Show college-specific roles for that college + default system roles
        - If no college_id: Show only default system roles
        """
        queryset = Role.objects.select_related('college')

        # Get college_id from query parameters
        college_id = self.request.query_params.get('college_id')

        # Filter by college_id if provided (applies to all users including superusers)
        if college_id:
            # Show college-specific roles + system default roles for that college
            queryset = queryset.filter(
                Q(college_id=college_id) | Q(college__isnull=True)
            )
        else:
            # Show only system default roles (no college specified)
            queryset = queryset.filter(college__isnull=True)

        # Query parameters for filtering
        is_default = self.request.query_params.get('is_default')
        is_active = self.request.query_params.get('is_active')

        if is_default is not None:
            queryset = queryset.filter(is_default=is_default.lower() == 'true')

        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')

        return queryset

    def create(self, request, *args, **kwargs):
        """Create new role"""
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response({
            'success': True,
            'message': 'Role created successfully',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """Update role"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # Allow updating any role (both default and custom)
        # Permissions can be assigned to all roles
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({
            'success': True,
            'message': 'Role updated successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """Delete role"""
        instance = self.get_object()

        # Check if role has active users (applies to all roles)
        active_users_count = instance.user_assignments.filter(is_active=True).count()
        if active_users_count > 0:
            return Response({
                'success': False,
                'message': f'Cannot delete role. {active_users_count} active users are assigned to this role.'
            }, status=status.HTTP_400_BAD_REQUEST)

        self.perform_destroy(instance)

        return Response({
            'success': True,
            'message': 'Role deleted successfully'
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get', 'put'], url_path='permissions')
    def permissions(self, request, pk=None):
        """
        GET /api/roles/{id}/permissions/
        - Get all permissions grouped by module with assignment status

        PUT /api/roles/{id}/permissions/
        - Assign permissions to role
        Request body: {"permission_ids": [1, 2, 3, ...]}
        """
        role = self.get_object()

        if request.method == 'GET':
            return self._get_role_permissions(role, request)
        elif request.method == 'PUT':
            return self._assign_permissions(role, request)

    def _get_role_permissions(self, role, request):
        """Get role permissions grouped by module"""
        # Get all permissions grouped by module
        permissions = Permission.objects.all().order_by('module', 'name')

        # Get currently assigned permission IDs for this role
        assigned_permission_ids = set(
            role.permissions.values_list('id', flat=True)
        )

        # Group permissions by module
        permissions_by_module = {}
        for permission in permissions:
            if permission.module not in permissions_by_module:
                permissions_by_module[permission.module] = {
                    'module': permission.module,
                    'module_name': permission.module.replace('_', ' ').title(),
                    'permissions': []
                }

            permissions_by_module[permission.module]['permissions'].append({
                'id': permission.id,
                'name': permission.name,
                'codename': permission.codename,
                'description': permission.description,
                'is_assigned': permission.id in assigned_permission_ids
            })

        return Response({
            'success': True,
            'data': {
                'role': {
                    'id': role.id,
                    'name': role.name,
                    'description': role.description
                },
                'permissions_by_module': list(permissions_by_module.values())
            }
        }, status=status.HTTP_200_OK)

    def _assign_permissions(self, role, request):
        """Assign permissions to role"""
        serializer = RolePermissionAssignSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': 'Invalid data',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        permission_ids = serializer.validated_data['permission_ids']

        # Clear existing permissions
        RolePermission.objects.filter(role=role).delete()

        # Assign new permissions
        role_permissions = []
        for permission_id in permission_ids:
            role_permissions.append(
                RolePermission(
                    role=role,
                    permission_id=permission_id
                )
            )

        RolePermission.objects.bulk_create(role_permissions)

        # Clear permission cache for all users with this role
        from apps.users.models import UserRoleAssignment
        user_ids = UserRoleAssignment.objects.filter(
            role=role,
            is_active=True
        ).values_list('user_id', flat=True)

        from django.core.cache import cache
        for user_id in user_ids:
            cache.delete(f'user_permissions_{user_id}')

        return Response({
            'success': True,
            'message': f'{len(permission_ids)} permissions assigned to role successfully'
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='permissions/bulk')
    def bulk_assign_permissions(self, request, pk=None):
        """
        POST /api/roles/{id}/permissions/bulk/
        - Bulk assign permissions by module

        Request body:
        {
            "permissions": {
                "attendance": [1, 2, 3, 4],
                "finance": [5, 6, 7]
            }
        }
        """
        role = self.get_object()
        serializer = RolePermissionBulkAssignSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': 'Invalid data',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        permissions_data = serializer.validated_data['permissions']

        # Flatten permission IDs
        all_permission_ids = []
        for module, permission_ids in permissions_data.items():
            all_permission_ids.extend(permission_ids)

        # Validate all permission IDs exist
        existing_count = Permission.objects.filter(id__in=all_permission_ids).count()
        if existing_count != len(all_permission_ids):
            return Response({
                'success': False,
                'message': 'Some permission IDs are invalid'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Clear existing permissions
        RolePermission.objects.filter(role=role).delete()

        # Assign new permissions
        role_permissions = []
        for permission_id in all_permission_ids:
            role_permissions.append(
                RolePermission(
                    role=role,
                    permission_id=permission_id,
                    college=request.user.college if request.user.college else None,
                    assigned_by=request.user
                )
            )

        RolePermission.objects.bulk_create(role_permissions)

        return Response({
            'success': True,
            'message': f'{len(all_permission_ids)} permissions assigned to role successfully'
        }, status=status.HTTP_200_OK)


class PermissionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Permission read operations

    GET /api/permissions/
    - List all permissions
    - Filter: ?module=attendance

    GET /api/permissions/{id}/
    - Get permission details

    GET /api/permissions/modules/
    - Get list of all modules
    """
    permission_classes = [IsAuthenticated, IsSuperadminOrAdmin]
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer

    def get_queryset(self):
        """Filter permissions by module"""
        queryset = Permission.objects.all().order_by('module', 'codename')

        module = self.request.query_params.get('module')
        if module:
            queryset = queryset.filter(module=module)

        return queryset

    def list(self, request, *args, **kwargs):
        """List all permissions"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            'success': True,
            'data': {
                'count': queryset.count(),
                'permissions': serializer.data
            }
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='modules')
    def modules(self, request):
        """
        GET /api/permissions/modules/
        - Get list of all modules with permission counts
        """
        modules = Permission.objects.values('module').annotate(
            permission_count=Count('id')
        ).order_by('module')

        module_list = [
            {
                'module': m['module'],
                'module_name': m['module'].replace('_', ' ').title(),
                'permission_count': m['permission_count']
            }
            for m in modules
        ]

        return Response({
            'success': True,
            'data': {
                'count': len(module_list),
                'modules': module_list
            }
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='grouped')
    def grouped(self, request):
        """
        GET /api/permissions/grouped/
        - Get all permissions grouped by module
        """
        permissions = Permission.objects.all().order_by('module', 'name')

        # Group by module
        permissions_by_module = {}
        for permission in permissions:
            if permission.module not in permissions_by_module:
                permissions_by_module[permission.module] = {
                    'module': permission.module,
                    'module_name': permission.module.replace('_', ' ').title(),
                    'permissions': []
                }

            permissions_by_module[permission.module]['permissions'].append({
                'id': permission.id,
                'name': permission.name,
                'codename': permission.codename,
                'description': permission.description
            })

        return Response({
            'success': True,
            'data': {
                'permissions_by_module': list(permissions_by_module.values())
            }
        }, status=status.HTTP_200_OK)
