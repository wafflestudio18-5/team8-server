"""
Django settings for podo_server project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os
from envparse import env
from dotenv import load_dotenv
import dj_database_url

load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

SECRET_KEY = env("DJANGO_SECRET_KEY", cast=str, default="local_key")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!


# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = env('DEBUG', cast=str, default='false') in ('true', 'True')
DEBUG_TOOLBAR = env('DEBUG_TOOLBAR', cast=str, default='false') in ('true', 'True')
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "*.podomarket.shop",
    '.ap-northeast-2.compute.amazonaws.com',
]

IS_PRODUCTION = env("IS_PRODUCTION", cast=str, default="false") in ('true', 'True')

CSRF_COOKIE_SECURE = IS_PRODUCTION
SESSION_COOKIE_SECURE = IS_PRODUCTION
SECURE_SSL_REDIRECT = IS_PRODUCTION
# Application definition

print("is production?", IS_PRODUCTION)

INSTALLED_APPS = [
    'podo_app.apps.PodoAppConfig',
    'user.apps.UserConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    )
}

if DEBUG_TOOLBAR:
    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')
    INTERNAL_IPS = ('127.0.0.1',)

ROOT_URLCONF = 'podo_server.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'podo_server.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
SYSTEM_ENV = os.environ.get('SYSTEM_ENV', None)


USE_PRODUCTION_DB = env("USE_PRODUCTION_DB", cast=str, default="false") in ('true', 'True')

if SYSTEM_ENV == 'GITHUB_WORKFLOW':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': '127.0.0.1',
            'PORT': 3306,
            'NAME': 'waffle_backend_assignment_2',
            'USER': 'root',
            'PASSWORD': 'password',
        }
    }
elif USE_PRODUCTION_DB:
    DATABASES = {
        # Parse `DATABASE_URL` environment variable
        "default": dj_database_url.config(
            default="mysql://waffle-backend:seminar@localhost:3306/podo_db"
        )
    }
else :
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': '127.0.0.1',
            'PORT': 3306,
            'NAME': 'podo_db',
            'USER': 'waffle-backend',
            'PASSWORD': 'seminar',
        }
    }

DATABASES['default']['OPTIONS'] = {'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'ko'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
