import os
from pathlib import Path
import environ
from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()

SITE_URL = os.getenv('SITE_URL')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.getenv('SECRET_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

GEOAPIFY_API_KEY = os.getenv('GEOAPIFY_API_KEY')
WEATHERAPI_API_KEY = os.getenv('WEATHERAPI_API_KEY')
# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True
PROD = False
ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = ['https://storyvord-back-end-d432tn3msq-uc.a.run.app']
INSTALLED_APPS = [
    'daphne',
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'rest_framework',
    'storages',
    'rest_framework_swagger',
    'django.contrib.sites',
    #'drf_yasg',                      # Yet Another Swagger generator,
    'crew',
    'client',
    'accounts',
    'project',
    'storyvord_calendar',
    'files',
    'tasks',
    'announcement',
    'notification',
    'callsheets',
    'corsheaders',
    'django.core.mail.backends.smtp',
    'drf_spectacular',
    'referral',
    'company',
    'inbox',
]

SITE_ID = 1


# Add Django REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        "dj_rest_auth.utils.JWTCookieAuthentication",
    ),
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
     'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',  # drf-spectacular settings
}
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=14),

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

}

JWT_AUTH = {
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
    'JWT_AUTH_COOKIE': None,
    # Other settings as per your requirements
}
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]
CORS_ALLOW_ALL_ORIGINS = True
ROOT_URLCONF = 'storyvord.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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
WSGI_APPLICATION = 'storyvord.wsgi.application'
ASGI_APPLICATION = "storyvord.asgi.application"

if PROD:
    DATABASES = {
        'default': {
                'ENGINE': 'django.db.backends.postgresql',
                "HOST": os.getenv('DATABASE_HOST'),
                'NAME': os.getenv('DATABASE_NAME'),
                'USER': os.getenv('DATABASE_USER'),
                'PASSWORD': os.getenv('DATABASE_PASSWORD'),
                'PORT': 5432
            }
    }
else:
    DATABASES = {
        'default': {
                'ENGINE': 'django.db.backends.postgresql',  #'django.db.backends.mysql',  # or
                "HOST": "127.0.0.1",
                'NAME': 'storyvord_db',
                'USER': 'froztyo0',
                'PASSWORD': 'password',
                'PORT': '5432' #5432
            }
    }


AUTH_USER_MODEL = "accounts.User"

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

#AUTH_USER_MODEL = 'core.User'
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
# DEFAULT_NO_REPLY_EMAIL = 'getvishalprajapati@gmail.com'
DEFAULT_FROM_EMAIL = 'getvishalprajapati@gmail.com'  # Update this line
ACCOUNT_ACTIVATION_DAYS = 7

# Consider adding settings for static and media files for production
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.azure_storage.AzureStorage",
        "OPTIONS": {
          'timeout': 20,
          'expiration_secs': 500,
        },
    },
    "staticfiles": {
        "BACKEND": "storages.backends.azure_storage.AzureStorage",
    },
}

AZURE_CONTAINER=os.getenv('AZURE_CONTAINERS')
AZURE_ACCOUNT_NAME=os.getenv('AZURE_ACCOUNT_NAMES')
AZURE_ACCOUNT_KEY=os.getenv('AZURE_ACCOUNT_KEYS')