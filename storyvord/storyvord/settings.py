import os
from pathlib import Path
import environ
# from google.cloud import secretmanager
from datetime import timedelta
from dotenv import load_dotenv
# Import the service_account module
from google.oauth2 import service_account
# Initialize django-environ
env = environ.Env()
# Reading .env file
environ.Env.read_env('')
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Load environment variables from .env file
load_dotenv()
SECRET_KEY = env('SECRET_KEY')
OPENAI_API_KEY = env('OPENAI_API_KEY')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = ['https://story-app.azurewebsites.net']
INSTALLED_APPS = [
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
    #'drf_yasg',                      # Yet Another Swagger generator,
    'crew',
    'client',
    'accounts',
    'project',
    'storyvord_calendar',
    'files',
    'tasks',
    'callsheets',
    'corsheaders',
    'djoser',
    'django.core.mail.backends.smtp',
    'drf_spectacular'
]


# DJOSER = {
#     'PASSWORD_RESET_CONFIRM_URL': 'auth/password/reset/confirm/{uid}/{token}',
#     'PASSWORD_CHANGED_EMAIL_CONFIRMATION': True,

#     'USER_CREATE_PASSWORD_RETYPE': True,
#     'SEND_ACTIVATION_EMAIL': True,
#     'ACTIVATION_URL': 'auth/activate/{uid}/{token}',
#     'SERIALIZERS': {},
#     'EMAIL': {
#         'activation': 'accounts.emails.CustomActivationEmail',
#     },
# }

DJOSER = {
    # 'LOGIN_FIELD': 'email',
    # 'USER_CREATE_PASSWORD_RETYPE':True,
    # 'ACTIVATION_URL':'activate/{uid}/{token}',
    # 'SEND_ACTIVATION_EMAIL':True,
    # 'SEND_CONFIRMATION_EMAIL':True,
    # 'PASSWORD_CHANGED_EMAIL_CONFIRMATION':True,
    # 'PASSWORD_RESET_CONFIRM_URL': 'password-reset/{uid}/{token}',
    # 'SET_PASSWORD_RETYPE': True,
    # 'PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND': True,
    # 'TOKEN_MODEL': None,       # To Delete User Must Set it to None
    # 'SERIALIZERS':{
    #     'user_create': 'accounts.serializers.UserCreateSerializer',
    #     'user': 'accounts.serializers.UserCreateSerializer',
    #     'user_delete': 'djoser.serializers.UserDeleteSerializer',
    # },
    # 'EMAIL': {
    #     'activation': 'accounts.email.ActivationEmail',
    #     'confirmation': 'accounts.email.ConfirmationEmail',
    #     'password_reset': 'accounts.email.PasswordResetEmail',
    #     'password_changed_confirmation': 'accounts.email.PasswordChangedConfirmationEmail',
    # },
}


# Add Django REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
     'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',  # drf-spectacular settings
}
SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('Bearer'),
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=2),
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
    'whitenoise.middleware.WhiteNoiseMiddleware',
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
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
# Get the database URL from the DATABASE_URL environment variable
database_url = env('DATABASE_URL')
# Get the database password from the DATABASE_PASSWORD environment variable
database_password = env('DATABASE_PASSWORD')
# Parse the database URL
db_config = env.db_url_config(database_url)
# Override the password component with the value from the DATABASE_PASSWORD environment variable
db_config['PASSWORD'] = database_password
db_config['OPTIONS'] = {'sslmode': 'require'}
# Replace with your actual project ID
project_id = 'apis-424409'

# uncomment it when use

# def access_secret_version(project_id, secret_id, version_id):
#     client = secretmanager.SecretManagerServiceClient()
#     name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
#     response = client.access_secret_version(name=name)
#     return response.payload.data.decode('UTF-8')

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'HOST': '/cloudsql/apis-424409:us-central1:storyvord',  # Unix socket path for Cloud SQL
    #     'NAME': access_secret_version(project_id, 'db_name', 'latest'),
    #     'USER': access_secret_version(project_id, 'db_user', 'latest'),
    #     'PASSWORD': access_secret_version(project_id, 'db_password', 'latest'),
    #     'PORT': '',  # Leave empty to use the default port for Unix socket
    # }

    #  'default': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'HOST': '/cloudsql/apis-424409:us-central1:storyvord',  # Unix socket path
    #     'NAME': access_secret_version(project_id, 'db_name', 'latest'),
    #     'USER': access_secret_version(project_id, 'db_user', 'latest'),
    #     'PASSWORD': access_secret_version(project_id, 'db_password', 'latest'),
    #     'PORT': '',  # Leave empty to use the default port for Unix socket
    # }
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     # 'HOST': '127.0.0.1',  # or the appropriate host for your database
    #     'HOST': '/cloudsql/apis-424409:us-central1:storyvord',
    #     'NAME': access_secret_version(project_id, 'db_name', 'latest'),  # Replace 'latest' with appropriate version_id
    #     'USER': access_secret_version(project_id, 'db_user', 'latest'),  # Replace 'latest' with appropriate version_id
    #     'PASSWORD': access_secret_version(project_id, 'db_password', 'latest'),
    #     # 'PORT': '1234',  # Default PostgreSQL port
    #     'PORT': '1234',
    # }

    # # storyvord_db LOCAL - POSTGRES...
    # 'default': {
    #         'ENGINE': 'django.db.backends.postgresql',
    #         "HOST": "127.0.0.1",
    #         'NAME': 'storyvord_db',
    #         'USER': 'postgres',
    #         'PASSWORD': 'root',
    #         'PORT': '5432' 
    #     }

    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR + '/db.sqlite3', # This is where you put the name of the db file.
    #              # If one doesn't exist, it will be created at migration time.
    # },

    'default': {
        'ENGINE': 'django.db.backends.postgresql',  #'django.db.backends.mysql',  # or
        'HOST': '/cloudsql/apis-424409:us-central1:storyvord',
        # "HOST": "127.0.0.1",
        'NAME': 'storyvord_db',
        'USER': 'storyvord',
        'PASSWORD': 'storyvord',
        # 'PORT': '1234'
        'PORT': '',  # Leave empty to use the default port for Unix socket
    }


}
AUTH_USER_MODEL = "accounts.User"
if os.getenv('DOCKER'):
    GS_CREDENTIALS_PATH = '/code/apis-gcp-storyvord.json'  # Path within the container
else:
    GS_CREDENTIALS_PATH = os.path.join(BASE_DIR, 'apis-gcp-storyvord.json')  # Path for local development
# Google Cloud Storage settings
DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
GS_BUCKET_NAME = 'storyvord-profile'
GS_CREDENTIALS = service_account.Credentials.from_service_account_file(GS_CREDENTIALS_PATH)
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
SENDGRID_API_KEY = env('SENDGRID_API_KEY')
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