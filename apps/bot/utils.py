import os
import django
from django.conf import settings

def setup_django():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    if not settings.configured:
        django.setup()
