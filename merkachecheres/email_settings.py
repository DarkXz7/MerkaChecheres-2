# email_settings.py

import os
from django.conf import settings

if not settings.configured:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app_merkachecheres.settings")  # Reemplaza 'sena' con el nombre de tu proyecto
    settings.configure()

EMAIL_BACKEND = settings.EMAIL_BACKEND
EMAIL_HOST = settings.EMAIL_HOST
EMAIL_PORT = settings.EMAIL_PORT
EMAIL_USE_TLS = settings.EMAIL_USE_SSL
EMAIL_HOST_USER = settings.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = settings.EMAIL_HOST_PASSWORD
DEFAULT_FROM_EMAIL = settings.EMAIL_HOST_USER