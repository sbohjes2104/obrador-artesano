import os
import dj_database_url
import socket
from pathlib import Path

# Parche para Railway: Forzar IPv4 para evitar errores de red (Errno 101)
orig_getaddrinfo = socket.getaddrinfo
def patched_getaddrinfo(*args, **kwargs):
    responses = orig_getaddrinfo(*args, **kwargs)
    return [res for res in responses if res[0] == socket.AF_INET]
socket.getaddrinfo = patched_getaddrinfo

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-@v%p#$*&^%#@!1234567890abcdefghijklmnopqrstuv'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'shop',
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

ROOT_URLCONF = 'obrador.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'obrador.wsgi.application'

# Database
# Use DATABASE_URL or MYSQL_URL for Railway/Production, default to local values
# Also try individual Railway variables if URL is missing
MYSQL_URL = os.environ.get('DATABASE_URL') or os.environ.get('MYSQL_URL')
if not MYSQL_URL and os.environ.get('MYSQLHOST'):
    MYSQL_URL = f"mysql://{os.environ.get('MYSQLUSER')}:{os.environ.get('MYSQLPASSWORD')}@{os.environ.get('MYSQLHOST')}:{os.environ.get('MYSQLPORT')}/{os.environ.get('MYSQLDATABASE')}"

DATABASES = {
    'default': dj_database_url.config(
        default=MYSQL_URL or f"mysql://{os.environ.get('DB_USER', 'obrador_user')}:{os.environ.get('DB_PASSWORD', 'obrador_password')}@{os.environ.get('DB_HOST', '127.0.0.1')}:{os.environ.get('DB_PORT', '3306')}/{os.environ.get('DB_NAME', 'obrador_db')}"
    )
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise storage to serve compressed files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Proxy settings for Railway
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

CSRF_TRUSTED_ORIGINS = [f"https://{host}" for host in os.environ.get('ALLOWED_HOSTS', '').split(',') if host and host != '*']
if not CSRF_TRUSTED_ORIGINS:
    CSRF_TRUSTED_ORIGINS = ["https://*.railway.app", "https://*.up.railway.app"]

# Media files
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Authentication URLs
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = 'login'

AUTHENTICATION_BACKENDS = [
    'core.backends.EmailOrUsernameModelBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# Configuración de Correo Electrónico
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.googlemail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 465))
# Si el puerto es 465, solemos usar SSL. Si es 587, usamos TLS.
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'False' if EMAIL_PORT == 465 else 'True').lower() == 'true'
EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL', 'True' if EMAIL_PORT == 465 else 'False').lower() == 'true'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')

# Correo desde el que se envían las notificaciones
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER)
# Correo que recibe los mensajes de contacto
CONTACT_EMAIL = os.environ.get('CONTACT_EMAIL', EMAIL_HOST_USER)

# Tiempo de espera para la conexión (evita cuelgues en Railway)
EMAIL_TIMEOUT = int(os.environ.get('EMAIL_TIMEOUT', 10))

