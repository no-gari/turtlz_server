import datetime
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'pj%2ze09(g)i^joilp-f8gvs)6ou_m036u3ejs^ky&9nse5k92'

ALLOWED_HOSTS = [
    '*.ap-northeast-2.elasticbeanstalk.com'
]

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
]

LOCAL_APPS = [
    'api.user.apps.UserConfig',
    'api.logger.apps.LoggerConfig',
    'api.commerce.apps.CommerceConfig',
    'api.magazine.apps.MagazineConfig',
    'api.community.apps.CommunityConfig',
]

THIRD_PARTY_APPS = [
    # 'storages',
    'rest_framework',
]

SITE_ID = 1

INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS

# HOST
DEFAULT_HOST = 'api'
ROOT_HOSTCONF = 'configs.hosts'
ROOT_URLCONF = 'configs.urls'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

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

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'ko'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

SITE_NAME = 'ustain'

STATIC_URL = '/static/'
STATIC_ROOT = 'static'

MEDIA_URL = '/media/'
MEDIA_ROOT = 'media'

# AUTH_USER_MODEL
AUTH_USER_MODEL = 'user.User'

# APPLICATION
WSGI_APPLICATION = 'configs.wsgi.application'
ASGI_APPLICATION = 'configs.asgi.application'

# JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(weeks=99999),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(weeks=99999),
    'ROTATE_REFRESH_TOKENS': True,
}

# DJANGO REST FRAMEWORK
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'api.user.serializers.login.CustomJWTAuthentication',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
        'djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'djangorestframework_camel_case.parser.CamelCaseFormParser',
        'djangorestframework_camel_case.parser.CamelCaseMultiPartParser',
        'djangorestframework_camel_case.parser.CamelCaseJSONParser',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
    'DATETIME_FORMAT': '%Y.%m.%d',
}

# SWAGGER
SWAGGER_SETTINGS = {
    'DEFAULT_AUTO_SCHEMA_CLASS': 'config.swagger.SquadSwaggerAutoSchema',
    'USE_SESSION_AUTH': True,
    'DOC_EXPANSION': 'list',
    'APIS_SORTER': 'alpha',
    'SECURITY_DEFINITIONS': None,
    'DEFAULT_API_URL': 'http://127.0.0.1:8000/docs'
}

# COOLSMS
COOLSMS_API_KEY = 'NCSMVIWDWDVLDXLG'
COOLSMS_API_SECRET = 'N9KGGSNNCBONQZAYKEP8QDIMPBISY8PS'
COOLSMS_FROM_PHONE = '01083589504'

# MAILGUN
MAILGUN_API_KEY = "a1209bfad6ca285a9ad2e0d7c1356b80-a0cfb957-2866bfcd"
MAILGUN_DOMAIN = "https://api.mailgun.net/v3/api.ustain.be"
MAILGUN_FROM_EMAIL = 'sofaissofa@icloud.com'


# KAKAO_LOGIN
KAKAO_API_KEY = '834031fe8f729b4ce1c4d1865bccd63a'

# CORS
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    # "clayful",
]
