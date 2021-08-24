from aiot_server_system.settings import *

SETTINGS_ENV = 'beta'

DEBUG = True
ALLOWED_HOSTS = ['*']

DATABASES['default']['USER'] = get_secret("DATABASE_USER_BETA")
DATABASES['default']['PASSWORD'] = get_secret("DATABASE_PASSWORD_BETA")
DATABASES['default']['HOST'] = get_secret("DATABASE_HOST_BETA")
DATABASES['default']['PORT'] = get_secret("DATABASE_PORT_BETA")

USER = 'http://aiot-server-user'
