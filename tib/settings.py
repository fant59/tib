import os
import environ

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ENV = environ.Env()
# ENV.read_env(os.path.join(BASE_DIR, "../.env"))

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = ENV.str('SECRET_KEY', '')

SECRET_KEY = 'i9zm2nawc!b_mh!@yj0xzp*(5_z%_ojotoc(qvtm21!s(rl=qs'
# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = ENV.bool('DEBUG', False)
DEBUG = True

# ALLOWED_HOSTS
# -----------------------------------------------------------------------------
ALLOWED_HOSTS = [
    '127.0.0.1',
]
# ips = ENV('IP').split(',')
# if ips:
#     ips = [i.strip() for i in ips]
#     ALLOWED_HOSTS += ips
# -----------------------------------------------------------------------------

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'sekizai',
    'rest_framework',

]

PROJECT_APPS = [
    'core',
    'reports',
    'reports.stocks',
    'reports.advice',
]

INSTALLED_APPS += PROJECT_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tib.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'sekizai.context_processors.sekizai',
            ],
        },
    },
]

WSGI_APPLICATION = 'tib.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    # 'default': ENV.db(),
    # 'default': ENV.db(),
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'trade_journal',
        'USER': 'fant_trade_journal',
        'PASSWORD': 'Torvv5cb',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# STATIC AND MEDIA
# -----------------------------------------------------------------------------
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'tib', 'static')
]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = "/static/"
MEDIA_URL = "/media/"
# -----------------------------------------------------------------------------

# REST_FRAMEWORK
# -----------------------------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
}

API_OBJECT = None
# TOKEN = ENV('TOKEN')
TOKEN = 't.2kKOIdYLs7EK__G-g6KOOouoT58u2xUL3rX_Z4CpFzIsne3mR1uqXsTfrf0rNQeUr-7ls8WDOLa2DfKipb_VRQ'
