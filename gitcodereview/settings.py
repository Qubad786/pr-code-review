"""
Django settings for gitcodereview project.
"""

import os
from os.path import abspath, dirname, join
from django.core.urlresolvers import reverse_lazy

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', True)

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'web',
    'web.pullrequest',
    'web.user',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'gitcodereview.urls'

# Custom user model
AUTH_USER_MODEL = "user.User"

AUTHENTICATION_BACKENDS = [
    'web.user.auth_backend.UserAuthenticationBackend',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'gitcodereview.wsgi.application'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

# Login URL
LOGIN_URL = reverse_lazy('index')

# Login Redirect URL
LOGIN_REDIRECT_URL = reverse_lazy('dashboard')

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Use developer's overrides if environment variables are not set.
if os.path.isfile(join(dirname(abspath(__file__)), 'private.py')):
    from private import *

# Secret key used in production secret.
SECRET_KEY = os.environ.get('SECRET_KEY', SECRET_KEY)

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', DB_NAME),
        'USER': os.environ.get('DB_USER', DB_USER),
        'PASSWORD': os.environ.get('DB_PASSWORD', DB_PASSWORD),
        'HOST': os.environ.get('DB_HOST', DB_HOST),
        'PORT': os.environ.get('DB_PORT', DB_PORT),
    }
}

# Github Oauth settings
OAUTH_SETTINGS = {
    'CLIENT_ID': os.environ.get('CLIENT_ID', CLIENT_ID),
    'CLIENT_SECRET': os.environ.get('CLIENT_SECRET', CLIENT_SECRET),
    'BASE_URL': os.environ.get('BASE_URL', BASE_URL),
    'ACCESS_TOKEN_URL': os.environ.get('ACCESS_TOKEN_URL', ACCESS_TOKEN_URL),
    'REDIRECT_URL': os.environ.get('REDIRECT_URL', REDIRECT_URL),
}
