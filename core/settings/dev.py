from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'secret'#'django-insecure-p^jj6n*clr_o*(y0ieazv_=%xcj)igx5=0gliiqdyt(pnacz^*'

# # https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
       'ENGINE': 'django.db.backends.mysql',
        'NAME': 'python_users_db',
        'USER': 'root',
        'PASSWORD': 'score2021@',
        'PORT': '3306',
        'HOST': 'localhost'

    }
}

'''CSRF_TRUSTED_ORIGINS = []
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = []
CORS_ORIGIN_REGEX_WHITELIST = []'''


CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:5173",
    "http://localhost:5173"
]

CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:5173/",
    "http://127.0.0.1:5173",
    "http://localhost:5173/",
    "http://localhost:5173",
]

CORS_ALLOWED_CREDENTIALS = True
CORS_EXPOSE_HEADERS = ["Content-Type", "X-CSRFToken"]
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTP_ONLY = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SAMESITE = 'None'