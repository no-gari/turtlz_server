import os
import datetime
import firebase_admin
from pathlib import Path
from firebase_admin import credentials

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'pj%2ze09(g)i^joilp-f8gvs)6ou_m036u3ejs^ky&9nse5k92'

ALLOWED_HOSTS = ['*.ap-northeast-2.elasticbeanstalk.com']

# BASE DJANGO APPS
DJANGO_APPS = [
    'admin_menu',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
]

# LOCAL API APPS
LOCAL_APPS = [
    'api.user.apps.UserConfig',
    'api.logger.apps.LoggerConfig',
    'api.notification.apps.NotificationConfig',
    # 'api.mypage.apps.MypageConfig',
    # 'api.magazine.apps.MagazineConfig',
    # 'api.firebase.apps.FirebaseConfig',
]

# COMMERCE API APPS
COMMERCE_APPS = [
    'api.commerce.cart.apps.CartConfig',
    'api.commerce.brand.apps.BrandConfig',
    'api.commerce.order.apps.OrderConfig',
    'api.commerce.review.apps.ReviewConfig',
    'api.commerce.search.apps.SearchConfig',
    'api.commerce.coupon.apps.CouponConfig',
    'api.commerce.comment.apps.CommentConfig',
    'api.commerce.product.apps.ProductConfig',
    'api.commerce.customer.apps.CustomerConfig',
    'api.commerce.collection.apps.CollectionConfig',
]

# OTHER LIBRARIES
THIRD_PARTY_APPS = [
    # DJANGO STORAGES FOR SERVER
    'storages',
    # DJANGO FILTER BACKEND
    'django_filters',
    # WYSIWYG EDITOR
    'django_summernote',
    # DRF
    'rest_framework',
    'rest_framework.authtoken',
    # DJANGO ELASTIC SEARRCH MODEL
    # 'django_elasticsearch_dsl',
]

INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + COMMERCE_APPS + THIRD_PARTY_APPS

# DJANGO BASE USER MODEL
SITE_ID = 1
AUTH_USER_MODEL = 'user.User'

# HOST
DEFAULT_HOST = 'api'
ROOT_HOSTCONF = 'configs.hosts'
ROOT_URLCONF = 'configs.urls'

# MIDDLEWARE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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

# ADMIN SITE NAME
SITE_NAME = 'ustain'

# BASE DJANGO LOCATION
LANGUAGE_CODE = 'ko'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_L10N = True
USE_TZ = False

# BASE STATIC, MEDIA ROOT
STATIC_URL = '/static/'
STATIC_ROOT = 'static'
MEDIA_URL = '/media/'
MEDIA_ROOT = 'media'

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
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # 'api.user.serializers.login.CustomJWTAuthentication',
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

# ELASTIC SEARCH
# ELASTICSEARCH_DSL={
#     'default': {
#         'hosts': 'localhost:9200'
#     },
# }


# SUMMERNOTE
SUMMERNOTE_CONFIG = {
    'iframe': True,
    'attachment_filesize_limit': 1024 * 1024 * 10  # 10MB
}
X_FRAME_OPTIONS = 'SAMEORIGIN'

# COOLSMS
# COOLSMS_API_KEY = 'NCSMVIWDWDVLDXLG'
# COOLSMS_API_SECRET = 'N9KGGSNNCBONQZAYKEP8QDIMPBISY8PS'
# COOLSMS_FROM_PHONE = '01083589504'

# MAILGUN
# MAILGUN_API_KEY = "a1209bfad6ca285a9ad2e0d7c1356b80-a0cfb957-2866bfcd"
# MAILGUN_DOMAIN = "https://api.mailgun.net/v3/api.ustain.be"
# MAILGUN_FROM_EMAIL = 'sofaissofa@icloud.com'

# FIREBASE PUSH NOTIFICATION
cred_path = os.path.join(BASE_DIR, "serviceAccountKey.json")
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)
