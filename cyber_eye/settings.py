from __future__ import absolute_import, unicode_literals  # For celery
import os
import django_heroku
from huey import RedisHuey
from redis import ConnectionPool

# Directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
ALLAUTH_DIR = os.path.join(BASE_DIR, 'templates', 'allauth')
DATABASE_DIR = os.path.join(BASE_DIR, 'db.sqlite3')

SECRET_KEY = os.environ.get('CYBER_EYE_SECRET_KEY')

DEBUG = (os.environ.get('DEBUG_VALUE') == 'True')


if DEBUG:
    ALLOWED_HOSTS = []
else:
    ALLOWED_HOSTS = ['cybereyeproject.herokuapp.com']
    # Security
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # django-allauth
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # The social providers
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.instagram',

    # Third party
    'crispy_forms',
    'huey.contrib.djhuey',

    # My apps
    'home.apps.HomeConfig',
    'users.apps.UsersConfig',
    'quiz.apps.QuizConfig',
    'social_media.apps.SocialMediaConfig',
]

# django-allauth
SITE_ID = 1
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"

# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        'APP': {
            'client_id': '123',
            'secret': '456',
            'key': ''
        }
    }
}

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

ROOT_URLCONF = 'cyber_eye.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR, ALLAUTH_DIR],
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

WSGI_APPLICATION = 'cyber_eye.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DATABASE_DIR,
    }
}

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

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


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CRISPY_TEMPLATE_PACK = 'bootstrap4'


# EMAIL
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = os.environ.get('DJANGO_EMAIL')
EMAIL_HOST_PASSWORD = os.environ.get('DJANGO_EMAIL_PASSWORD')
EMAIL_PORT = 587


# Huey task queue settings
# https://huey.readthedocs.io/en/latest/django.html
# pool = ConnectionPool(host='my.redis.host', port=6379, max_connections=20)
# HUEY = RedisHuey('my-app', connection_pool=pool, immediate_use_memory=False)

# HUEY = {
#     'huey_class': 'huey.SqliteHuey',
#     'name': DATABASES['default']['NAME'],
#     'immediate': False,
    # Options to pass into the consumer when running ``manage.py run_huey``
    # 'consumer': {
    #     'workers': 4,
    #     'worker_type': 'thread',
    # },
# }

# url = 'redis://h:pc42c38ab33253d80428caf0f6f503b1750a681280c06110d9aa38fa0de0a44a4@ec2-34-204-117-137.compute-1.amazonaws.com:7599'
# HUEY = RedisHuey('my-app', host=url)
# Keep this at the very bottom of the file - This sets a lot of configs for django and heroku
django_heroku.settings(locals())


"""
Write stuff to make file commit
"""

