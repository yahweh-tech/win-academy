"""
Django settings for WIN PROFESSIONAL ACADEMY platform.
Production-ready configuration supporting PostgreSQL, S3-Compatible Object Storage,
WhiteNoise static files, and customizable environment variables.
"""

import os
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file if present
load_dotenv(BASE_DIR / '.env')

# Quick-start development settings - unsuitable for production
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-win-academy-prod-dev-key-change-in-production-^!#8893923'
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True').lower() in ('true', '1', 'yes')

ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1,0.0.0.0,.onrender.com').split(',')
    if host.strip()
]

# CSRF Trusted Origins for Render & Custom Domains
CSRF_TRUSTED_ORIGINS_RAW = os.environ.get(
    'CSRF_TRUSTED_ORIGINS',
    'http://localhost:8000,http://127.0.0.1:8000,https://*.onrender.com'
)
CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in CSRF_TRUSTED_ORIGINS_RAW.split(',')
    if origin.strip()
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third party
    'storages',
    # Academy application
    'academy.apps.AcademyConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'academy.context_processors.academy_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database configuration
# Support PostgreSQL through DATABASE_URL (Render, Docker, local postgres)
# Fallback to SQLite for zero-config local quick testing if DATABASE_URL is not set
DEFAULT_DATABASE_URL = f"sqlite:///{BASE_DIR / 'db.sqlite3'}"
DATABASE_URL = os.environ.get('DATABASE_URL', DEFAULT_DATABASE_URL)

DATABASES = {
    'default': dj_database_url.config(
        default=DATABASE_URL,
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8},
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise storage configuration
STATICFILES_STORAGE_BACKEND = (
    "whitenoise.storage.CompressedStaticFilesStorage"
    if (DEBUG or os.environ.get('DJANGO_TESTING') == '1' or 'test' in os.sys.argv)
    else "whitenoise.storage.CompressedManifestStaticFilesStorage"
)

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": STATICFILES_STORAGE_BACKEND,
    },
}

# Media & Persistent Object Storage Configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Check if Object Storage is configured (S3-compatible: Cloudflare R2, AWS S3, Backblaze B2, Supabase)
USE_S3_STORAGE = os.environ.get('USE_S3_STORAGE', 'False').lower() in ('true', '1', 'yes') or bool(
    os.environ.get('STORAGE_ACCESS_KEY') or os.environ.get('AWS_ACCESS_KEY_ID')
)

if USE_S3_STORAGE:
    AWS_ACCESS_KEY_ID = os.environ.get('STORAGE_ACCESS_KEY') or os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('STORAGE_SECRET_KEY') or os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('STORAGE_BUCKET_NAME') or os.environ.get('AWS_STORAGE_BUCKET_NAME', 'win-academy-media')
    AWS_S3_REGION_NAME = os.environ.get('STORAGE_REGION') or os.environ.get('AWS_S3_REGION_NAME', 'auto')
    
    # Custom endpoint for S3-compatible services (Cloudflare R2, MinIO, Wasabi, Backblaze)
    AWS_S3_ENDPOINT_URL = os.environ.get('STORAGE_ENDPOINT_URL')
    
    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = None
    AWS_QUERYSTRING_AUTH = False
    
    # Optional custom domain for CDN
    AWS_S3_CUSTOM_DOMAIN = os.environ.get('STORAGE_CUSTOM_DOMAIN')
    if AWS_S3_CUSTOM_DOMAIN:
        MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/media/public/"
    elif AWS_S3_ENDPOINT_URL and 'r2.cloudflarestorage.com' not in AWS_S3_ENDPOINT_URL:
        MEDIA_URL = f"{AWS_S3_ENDPOINT_URL}/{AWS_STORAGE_BUCKET_NAME}/media/public/"
    
    STORAGES["default"] = {
        "BACKEND": "config.storage_backends.PublicMediaStorage",
    }

# File Upload limits (Max 50MB)
DATA_UPLOAD_MAX_MEMORY_SIZE = 52428800  # 50 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 52428800  # 50 MB

# Production Security Settings
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'True').lower() in ('true', '1', 'yes')
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'True').lower() in ('true', '1', 'yes')
    CSRF_COOKIE_SECURE = os.environ.get('CSRF_COOKIE_SECURE', 'True').lower() in ('true', '1', 'yes')
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = int(os.environ.get('SECURE_HSTS_SECONDS', 31536000))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
