from CADHU.settings.common import *
import os
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '04x+s_*qi^^=g)y6x)^j_1dadrv$wg))5pico59(+&est)c8t%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
