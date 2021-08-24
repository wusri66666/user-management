import os

from django.core.wsgi import get_wsgi_application

env = os.environ.get('ENV')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aiot_server_system.%s"%env)
application = get_wsgi_application()