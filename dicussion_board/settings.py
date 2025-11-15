import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

def get_env(var_name, default=None):
    return os.environ.get(var_name, default)

# SECRET_KEY
SECRET_KEY = get_env("SECRET_KEY", "REPLACED_SECRET_KEY")

# DEBUG
DEBUG = get_env("DEBUG", "False").lower() in ("1", "true", "yes")

# ALLOWED_HOSTS
ALLOWED_HOSTS = get_env("ALLOWED_HOSTS", "").split(",") if get_env("ALLOWED_HOSTS") else ["*"]

# Database
DATABASE_URL = get_env("DATABASE_URL")
if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    }
else:
    # fallback local
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'Boards_django',
            'USER': 'postgres',
            'PASSWORD': 'PASSWORD',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR/'static']

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # لضمان خدمة static على الإنتاج
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Authentication URLs
LOGOUT_REDIRECT_URL = 'home'
LOGIN_REDIRECT_URL = 'home'
LOGIN_URL = 'login'




