from CADHU.settings.common import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['sistemacadhu.com','159.89.229.54']

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'cadhu',
        'USER': 'cadhu',
        'PASSWORD': '8qX8vx1P*Xpu',
        'HOST': 'sistemacadhu.com',
        'PORT': '5432',
    }
}
