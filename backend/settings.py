from pathlib import Path
from decouple import AutoConfig

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Decouple lê o .env dentro do projeto
config = AutoConfig(search_path=BASE_DIR)

DEBUG = config('DEBUG', default=False, cast=bool)
SECRET_KEY = config('SECRET_KEY', default='change-me')

# Banco de dados: por padrão, use SQLite
DEFAULT_DB_SQLITE = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': BASE_DIR / 'db.sqlite3',
}

USE_POSTGRES = config('USE_POSTGRES', default=False, cast=bool)

if USE_POSTGRES:
    # Só usa Postgres se todas as credenciais estiverem definidas
    db_name = config('DB_NAME', default='')
    db_user = config('DB_USER', default='')
    db_password = config('DB_PASSWORD', default='')
    db_host = config('DB_HOST', default='')
    db_port = config('DB_PORT', default='5432')

    if all([db_name, db_user, db_password, db_host]):
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': db_name,
                'USER': db_user,
                'PASSWORD': db_password,
                'HOST': db_host,
                'PORT': db_port,
            }
        }
    else:
        DATABASES = {'default': DEFAULT_DB_SQLITE}
else:
    DATABASES = {'default': DEFAULT_DB_SQLITE}

CONN_MAX_AGE = config('DB_CONN_MAX_AGE', default=60, cast=int)
# Fallback para SQLite no PythonAnywhere free
if config('PA_USE_SQLITE', default=True, cast=bool):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME', default='clone_x'),
            'USER': config('DB_USER', default='clone_x'),
            'PASSWORD': config('DB_PASSWORD', default='Nicolas-157'),
            'HOST': config('DB_HOST', default='localhost'),
            'PORT': config('DB_PORT', default='5432'),
        }
    }