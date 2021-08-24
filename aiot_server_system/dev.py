from aiot_server_system.settings import *

SETTINGS_ENV = 'dev'

DEBUG = True
ALLOWED_HOSTS = ['*']

DATABASES['default']['USER'] = get_secret("DATABASE_USER_DEV")
DATABASES['default']['PASSWORD'] = get_secret("DATABASE_PASSWORD_DEV")
DATABASES['default']['HOST'] = get_secret("DATABASE_HOST_DEV")
DATABASES['default']['PORT'] = get_secret("DATABASE_PORT_DEV")

USER = 'http://api.dev.smartahc.com/aiot/v2/user'