"""
Middleware for handling multi-school database routing.
Extracts school selection from request headers/params and sets database context.
"""
from django.utils.deprecation import MiddlewareMixin
from .db_router import SchoolDatabaseRouter


class SchoolDatabaseMiddleware(MiddlewareMixin):
    """
    Middleware to set the school context for database routing.
    Extracts school_id from:
    1. Header: X-School-Id
    2. Query parameter: school_id
    3. Session data: school_id
    """

    def process_request(self, request):
        """
        Set the school context before processing the request.
        """
        # Skip database routing for authentication endpoints
        if request.path.startswith('/api/auth/'):
            # For auth endpoints, use default database only
            SchoolDatabaseRouter.set_school('school1')
            return None

        # Try to get school_id from various sources
        school_id = (
            request.headers.get('X-School-Id') or
            request.GET.get('school_id') or
            request.POST.get('school_id') or
            'school1'  # Default to school1
        )

        # Try to get from session if available
        try:
            if hasattr(request, 'session') and request.session:
                school_id = request.session.get('school_id', school_id)
        except Exception:
            # Session might not be initialized yet
            pass

        # Validate school_id - accept both college IDs (1, 2) and school names (school1, school2)
        valid_schools = ['school1', 'school2', '1', '2']
        if school_id not in valid_schools:
            school_id = 'school1'
        # Convert college IDs to school database names if needed
        elif school_id == '1':
            school_id = 'school1'
        elif school_id == '2':
            school_id = 'school2'

        # Set the school context for database operations
        SchoolDatabaseRouter.set_school(school_id)

        # Try to store in session for persistence
        try:
            if hasattr(request, 'session') and request.session:
                request.session['school_id'] = school_id
        except Exception:
            # Session might not be available
            pass

        return None

    def process_response(self, request, response):
        """
        Clean up after request processing.
        """
        # Clear the thread-local school context
        SchoolDatabaseRouter.clear_school()
        return response
