"""
App configuration for validation app
"""
from django.apps import AppConfig


class ValidationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'validation'
