import dj_database_url
import os
import django_heroku

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "ro5rd^(wia%&wji)uc@st(6l@e)-^0e$o*wx-3w=v8^!6m=d%e"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", "iblinkco-django.herokuapp.com"]


# Application definition

INSTALLED_APPS = [
    # Project Apps
    'homepage.apps.HomepageConfig',
    'billing.apps.BillingConfig',
    'management.apps.ManagementConfig',
    'blog.apps.BlogConfig',
    'dashboard.apps.DashboardConfig',
    'users.apps.UsersConfig',
    'service.apps.ServiceConfig',
    'chat.apps.ChatConfig',
    'channels',
    # 'whitenoise.runserver_nostatic',

    # Django libraries
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Other libs
    'crispy_forms',
    'storages',
    'six'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware',

]

ROOT_URLCONF = 'webapp.urls'

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
# AUTH_USER_MODEL = 'users.Account'
WSGI_APPLICATION = 'webapp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
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


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# Media Settings
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

#Email Settings
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_HOST_USER = "confirmemailiblinkco@gmail.com"
EMAIL_HOST_PASSWORD = "598E,?^r%}UanaW'"

AUTHENTICATION_BACKENDS = (
    # 'django.contrib.auth.backends.ModelBackend',
    'users.backends.EmailBackend',
    # 'django.contrib.auth.backends.ModelBackend',
)

# Channels
ASGI_APPLICATION = 'webapp.routing.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": ["redis://h:954c886918c238905dc2c322c34546bd9dbc2738d32523b12bc36ed2d058c387ec@ec2-34-211-446-320.compute-1.amazonaws.com:7719"],
        },
    },
}

if os.getcwd() =='/app':
    DEBUG=False


django_heroku.settings(locals())

# Stripe
STRIPE_PUBLISHABLE_KEY = 'pk_test_S49pZhR9n8Qm0MM34RGzsMyG'
STRIPE_SECRET_KEY = 'sk_test_8dRE7QLn40wUt6wZtr8upMA4'
STRIPE_CONNECT_CLIENT_ID = 'ca_HBCiaAX9Br1gw4YiOtDI0McQffyqVTxz'

# AWS E3
AWS_ACCESS_KEY_ID = "AKIA3YGF6HNLB6JBJQHU"
AWS_SECRET_ACCESS_KEY = "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"
AWS_STORAGE_BUCKET_NAME = "iblinkco-django"
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Celery 
CELERY_BROKER_URL = 'redis://h:p433bdebe493ed86f7b09195c7983f3743ad34351fc6a892be0ac374927395332@ec2-3-81-254-48.compute-1.amazonaws.com:8879'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
