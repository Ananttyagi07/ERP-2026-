"""
User Management views
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


class UserManagementViewSet(viewsets.ViewSet):
    """
    User management operations:
    - List/filter users
    - Toggle active/inactive status
    - View user details
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """
        List all users with filters
        Query params:
        - college_id: Filter by college
        - user_type: Filter by role (Admin, Teacher, Student, Guardian, Staff, etc.)
        - search: Search by name, email, username
        - is_active: Filter by active status
        """
        queryset = User.objects.select_related('college', 'department').all()

        # Filter by college
        college_id = request.query_params.get('college_id')
        if college_id:
            queryset = queryset.filter(college_id=college_id)

        # Filter by user type (role)
        user_type = request.query_params.get('user_type')
        if user_type:
            from apps.users.models import UserRoleAssignment
            role_user_ids = UserRoleAssignment.objects.filter(
                role__name=user_type,
                is_active=True
            ).values_list('user_id', flat=True)
            queryset = queryset.filter(id__in=role_user_ids)

        # Filter by active status
        is_active = request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')

        # Search
        search = request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search) |
                Q(username__icontains=search)
            )

        # Serialize
        data = []
        for user in queryset:
            primary_role = user.get_primary_role()
            data.append({
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'full_name': user.get_full_name(),
                'phone': user.phone,
                'college_id': user.college_id,
                'college_name': user.college.name if user.college else None,
                'is_active': user.is_active,
                'role': primary_role.name if primary_role else None,
                'avatar_url': request.build_absolute_uri(user.avatar.url) if user.avatar else None,
                'created_at': user.created_at,
            })

        return Response({
            'success': True,
            'data': {
                'count': len(data),
                'users': data
            }
        }, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Get user details"""
        try:
            user = User.objects.select_related('college', 'department').get(pk=pk)
        except User.DoesNotExist:
            return Response({
                'success': False,
                'message': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)

        primary_role = user.get_primary_role()

        data = {
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone': user.phone,
            'college_id': user.college_id,
            'college_name': user.college.name if user.college else None,
            'department_id': user.department_id,
            'department_name': user.department.name if user.department else None,
            'is_active': user.is_active,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
            'role': primary_role.name if primary_role else None,
            'avatar_url': request.build_absolute_uri(user.avatar.url) if user.avatar else None,
            'created_at': user.created_at,
        }

        return Response({
            'success': True,
            'data': data
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def toggle_status(self, request, pk=None):
        """Toggle user active/inactive status"""
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({
                'success': False,
                'message': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)

        user.is_active = not user.is_active
        user.save()

        return Response({
            'success': True,
            'message': f'User {"activated" if user.is_active else "deactivated"} successfully',
            'data': {
                'user_id': user.id,
                'is_active': user.is_active
            }
        }, status=status.HTTP_200_OK)


class ResetPasswordView(APIView):
    """Reset user password"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Reset password for any user
        Required fields:
        - college_id
        - user_type (role name)
        - user_id
        - new_password
        """
        college_id = request.data.get('college_id')
        user_type = request.data.get('user_type')
        user_id = request.data.get('user_id')
        new_password = request.data.get('new_password')

        if not all([college_id, user_type, user_id, new_password]):
            return Response({
                'success': False,
                'message': 'Missing required fields: college_id, user_type, user_id, new_password'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id, college_id=college_id)
        except User.DoesNotExist:
            return Response({
                'success': False,
                'message': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)

        # Set new password (will be hashed automatically)
        user.set_password(new_password)
        user.save()

        return Response({
            'success': True,
            'message': 'Password reset successfully',
            'data': {
                'user_id': user.id,
                'email': user.email,
                'username': user.username
            }
        }, status=status.HTTP_200_OK)


class ResetUsernameView(APIView):
    """Reset username"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Reset username for any user
        Required fields:
        - college_id
        - user_type
        - user_id
        - new_username
        """
        college_id = request.data.get('college_id')
        user_type = request.data.get('user_type')
        user_id = request.data.get('user_id')
        new_username = request.data.get('new_username')

        if not all([college_id, user_type, user_id, new_username]):
            return Response({
                'success': False,
                'message': 'Missing required fields: college_id, user_type, user_id, new_username'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Check if username already exists
        if User.objects.filter(username=new_username).exclude(id=user_id).exists():
            return Response({
                'success': False,
                'message': 'Username already exists'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id, college_id=college_id)
        except User.DoesNotExist:
            return Response({
                'success': False,
                'message': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)

        old_username = user.username
        user.username = new_username
        user.save()

        return Response({
            'success': True,
            'message': 'Username reset successfully',
            'data': {
                'user_id': user.id,
                'old_username': old_username,
                'new_username': new_username,
                'email': user.email
            }
        }, status=status.HTTP_200_OK)


class ViewCredentialsView(APIView):
    """View user credentials"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Get user credentials list
        Query params:
        - college_id
        - user_type (optional)
        - search (optional)
        """
        college_id = request.query_params.get('college_id')
        if not college_id:
            return Response({
                'success': False,
                'message': 'college_id is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        queryset = User.objects.filter(college_id=college_id).select_related('college', 'department')

        # Filter by user type
        user_type = request.query_params.get('user_type')
        if user_type:
            from apps.users.models import UserRoleAssignment
            role_user_ids = UserRoleAssignment.objects.filter(
                role__name=user_type,
                is_active=True
            ).values_list('user_id', flat=True)
            queryset = queryset.filter(id__in=role_user_ids)

        # Search
        search = request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search) |
                Q(username__icontains=search)
            )

        # Build response
        data = []
        for user in queryset:
            primary_role = user.get_primary_role()

            # Get profile-specific information
            profile_data = {}
            if hasattr(user, 'teacher_profile'):
                profile = user.teacher_profile
                profile_data = {
                    'national_id': profile.national_id,
                    'designation': profile.designation.name if profile.designation else None,
                    'department': user.department.name if user.department else None,
                    'joining_date': profile.joining_date,
                    'blood_group': profile.blood_group,
                    'religion': profile.religion,
                    'birth_date': profile.birth_date,
                    'present_address': profile.present_address,
                    'permanent_address': profile.permanent_address,
                    'gender': getattr(user, 'gender', ''),
                }
            elif hasattr(user, 'student_profile'):
                profile = user.student_profile
                profile_data = {
                    'roll_number': profile.roll_number,
                    'registration_number': profile.registration_number,
                    'class': profile.school_class.name if profile.school_class else None,
                    'section': profile.section.name if profile.section else None,
                    'admission_date': profile.admission_date,
                }

            data.append({
                'id': user.id,
                'college_name': user.college.name if user.college else None,
                'username': user.username,
                'password': '********',  # Masked password
                'full_name': user.get_full_name(),
                'email': user.email,
                'phone': user.phone,
                'role': primary_role.name if primary_role else None,
                'photo_url': request.build_absolute_uri(user.avatar.url) if user.avatar else None,
                **profile_data
            })

        return Response({
            'success': True,
            'data': {
                'count': len(data),
                'credentials': data
            }
        }, status=status.HTTP_200_OK)
