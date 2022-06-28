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
    'api.magazine.apps.MagazineConfig',
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
SITE_NAME = 'TURTLZ'

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

# SUMMERNOTE
SUMMERNOTE_CONFIG = {
    'iframe': True,
    'attachment_filesize_limit': 1024 * 1024 * 10  # 10MB
}
X_FRAME_OPTIONS = 'SAMEORIGIN'

# FIREBASE PUSH NOTIFICATION
cred_path = os.path.join(BASE_DIR, "serviceAccountKey.json")
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)

# CLAYFUL
CLAYFUL_API_KEY = '3c108f19f21895ebc6025900d41edebfd96df973afdd30f1c06471febad697e9ea7957f6'
CLAYFUL_API_SECRET = '4bac51a103b47d0be99020e0531a699105a86f1dbe57cf49eebcc888ce354e1d2eef4387aeb2139d9d3103e0245f3f99'
CLAYFUL_BACKEND_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjFlNzYzZDc4NTA2YTJiYmM3Y2NmZTcwMmM0ZWI3M2ExMzkyNjI2MTFmYjU4MzdiY2U0YzdiOTUxNGRkZmMwNzQiLCJyb2xlIjoiY2xpZW50IiwiaWF0IjoxNjU1ODA2NDMyLCJzdG9yZSI6IlpDSjRQOENaSDJVUi5HWjVRTFZIUVk1WFEiLCJzdWIiOiJORUY1VFdFNU1FRUwifQ.OT7C_v_38T3-ZR0AdQEpRi4OonnI18bev4G_os7ne40'
CLAYFUL_CAMPING_ID = 'SPM6WUPJG5MQ'
CLAYFUL_COLLECTION_ID = 'BR9KT8ZJPSFK'
CLAYFUL_BANNER_ID = 'DAZCMCFDX2Z2'
CLAYFUL_SHIPPING_ID = 'B6Q2MLNJ5RJ9'
CLAYFUL_COUPON_ID = 'QF32EJB45DH9'
CLAYFUL_PAYMENT_METHOD = '5F5G4WCZMAVS'

# IAMPORT
IAMPORT_CODE = 'imp30008433'
IAMPORT_KEY = '0330942419168537'
IAMPORT_SECRET = 'iogg8L0d5kh3MwuXrDAi9V3uZ7uNzP9Seq8nc8AhtSlfpQdRtO9DJc7IkBwUrFMF6V2i3DAwvVMUM0Lf'
IMPORT_EXPORT_USE_TRANSACTIONS = True
