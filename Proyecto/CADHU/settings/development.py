from CADHU.settings.common import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '04x+s_*qi^^=g)y6x)^j_1dadrv$wg))5pico59(+&est)c8t%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'cadhu',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
