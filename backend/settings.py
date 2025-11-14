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
