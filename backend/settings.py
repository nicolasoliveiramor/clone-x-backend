from pathlib import Path
from decouple import AutoConfig

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Decouple lê o .env dentro do projeto
config = AutoConfig(search_path=BASE_DIR)

DEBUG = config('DEBUG', default=False, cast=bool)
SECRET_KEY = config('SECRET_KEY', default='change-me')

DEFAULT_DB_SQLITE = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': BASE_DIR / 'db.sqlite3',
}

USE_POSTGRES = config('USE_POSTGRES', default=False, cast=bool)
PA_USE_SQLITE = config('PA_USE_SQLITE', default=True, cast=bool)

if PA_USE_SQLITE:
    DATABASES = {'default': DEFAULT_DB_SQLITE}
elif USE_POSTGRES:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME', default=''),
            'USER': config('DB_USER', default=''),
            'PASSWORD': config('DB_PASSWORD', default=''),
            'HOST': config('DB_HOST', default=''),
            'PORT': config('DB_PORT', default='5432'),
        }
    }
else:
    DATABASES = {'default': DEFAULT_DB_SQLITE}

CONN_MAX_AGE = config('DB_CONN_MAX_AGE', default=60, cast=int)

PA_HOST = config('PA_HOST', default='')
ALLOW_PYTHONANYWHERE_WILDCARD = config('ALLOW_PYTHONANYWHERE_WILDCARD', default=False, cast=bool)
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
if PA_HOST:
    ALLOWED_HOSTS.append(PA_HOST)
if ALLOW_PYTHONANYWHERE_WILDCARD:
    ALLOWED_HOSTS += ['.pythonanywhere.com']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'accounts',
    'posts',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'
WSGI_APPLICATION = 'backend.wsgi.application'

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

AUTH_USER_MODEL = 'accounts.User'

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

CSRF_TRUSTED_ORIGINS = []
if PA_HOST:
    CSRF_TRUSTED_ORIGINS.append(f"https://{PA_HOST}")
if ALLOW_PYTHONANYWHERE_WILDCARD:
    CSRF_TRUSTED_ORIGINS += ["https://*.pythonanywhere.com"]

CORS_ALLOW_ALL_ORIGINS = True
FRONTEND_ORIGIN = config('FRONTEND_ORIGIN', default='')
FRONTEND_ORIGIN_REGEX = config('FRONTEND_ORIGIN_REGEX', default='')
if FRONTEND_ORIGIN:
    CORS_ALLOW_ALL_ORIGINS = False
    CORS_ALLOWED_ORIGINS = [FRONTEND_ORIGIN]
    CORS_ALLOW_CREDENTIALS = True
    CSRF_TRUSTED_ORIGINS.append(FRONTEND_ORIGIN)
elif FRONTEND_ORIGIN_REGEX:
    CORS_ALLOW_ALL_ORIGINS = False
    CORS_ALLOWED_ORIGIN_REGEXES = [FRONTEND_ORIGIN_REGEX]
    CORS_ALLOW_CREDENTIALS = True
    if 'vercel.app' in FRONTEND_ORIGIN_REGEX:
        CSRF_TRUSTED_ORIGINS.append('https://*.vercel.app')

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'None'
CSRF_COOKIE_SAMESITE = 'None'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
