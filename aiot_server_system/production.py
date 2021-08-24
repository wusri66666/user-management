from aiot_server_system.settings import *

SETTINGS_ENV = 'production'

DEBUG = True
ALLOWED_HOSTS = ['*']

DATABASES['default']['USER'] = get_secret("DATABASE_USER_PRODUCTION")
DATABASES['default']['PASSWORD'] = get_secret("DATABASE_PASSWORD_PRODUCTION")
DATABASES['default']['HOST'] = get_secret("DATABASE_HOST_PRODUCTION")
DATABASES['default']['PORT'] = get_secret("DATABASE_PORT_PRODUCTION")

USER = 'http://aiot-server-user'
