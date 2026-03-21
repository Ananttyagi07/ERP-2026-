"""
Custom exception handlers for the API
"""
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """
    Custom exception handler that provides consistent error responses
    """
    # Call REST framework's default exception handler first to get the standard error response.
    response = exception_handler(exc, context)

    if response is None:
        return None

    # Customize response format
    if response.status_code == status.HTTP_401_UNAUTHORIZED:
        response.data = {
            'success': False,
            'message': 'Authentication credentials were not provided or are invalid.',
            'errors': response.data
        }
    elif response.status_code == status.HTTP_403_FORBIDDEN:
        response.data = {
            'success': False,
            'message': 'You do not have permission to perform this action.',
            'errors': response.data
        }
    elif response.status_code == status.HTTP_404_NOT_FOUND:
        response.data = {
            'success': False,
            'message': 'The requested resource was not found.',
            'errors': response.data
        }
    elif response.status_code == status.HTTP_400_BAD_REQUEST:
        response.data = {
            'success': False,
            'message': 'Invalid request. Please check your input.',
            'errors': response.data
        }
    elif response.status_code >= 500:
        response.data = {
            'success': False,
            'message': 'Internal server error occurred.',
            'errors': response.data
        }
    else:
        # For other errors, wrap in standard format if not already
        if isinstance(response.data, dict) and 'success' not in response.data:
            response.data = {
                'success': False,
                'message': 'An error occurred.',
                'errors': response.data
            }

    return response
