"""
FrontOffice app configuration
"""
from django.apps import AppConfig


class FrontOfficeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.front_office'
    verbose_name = 'FrontOffice'
