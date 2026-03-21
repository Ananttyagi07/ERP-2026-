"""
Permission and authentication middleware
"""
from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache


class PermissionMiddleware(MiddlewareMixin):
    """
    Middleware to load user permissions and role info into request
    Caches permissions for performance
    """

    def process_request(self, request):
        """
        Load user permissions if authenticated
        """
        if request.user.is_authenticated:
            # Load user permissions
            request.user_permissions = request.user.get_permissions()

            # Load user's primary role
            request.user_role = request.user.get_primary_role()

            # Add helper method to request
            request.has_permission = lambda perm: request.user.has_permission(perm)

        return None


class RequestLoggingMiddleware(MiddlewareMixin):
    """
    Middleware to log API requests (optional for audit)
    """

    def process_request(self, request):
        """Log incoming request"""
        if request.user.is_authenticated:
            # Store request metadata for audit logging
            request.audit_metadata = {
                'user_id': request.user.id,
                'user_email': request.user.email,
                'ip_address': self.get_client_ip(request),
                'user_agent': request.META.get('HTTP_USER_AGENT', ''),
                'method': request.method,
                'path': request.path,
            }
        return None

    @staticmethod
    def get_client_ip(request):
        """Extract client IP"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
