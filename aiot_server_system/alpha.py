from aiot_server_system.settings import *

SETTINGS_ENV = 'alpha'

DEBUG = True
ALLOWED_HOSTS = ['*']

DATABASES['default']['USER'] = get_secret("DATABASE_USER_ALPHA")
DATABASES['default']['PASSWORD'] = get_secret("DATABASE_PASSWORD_ALPHA")
DATABASES['default']['HOST'] = get_secret("DATABASE_HOST_ALPHA")
DATABASES['default']['PORT'] = get_secret("DATABASE_PORT_ALPHA")

USER = 'http://aiot-server-user.aiot-be-alpha'