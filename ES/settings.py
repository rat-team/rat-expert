"""
Django settings for ES project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

PROJECT_NAME = "es"

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
_PATH = os.path.abspath(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'dpp#zd_v1hqcy*fm7lxc3xush6uvij1m*7l#4ydxeobv_b^3!5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DEPLOY = False

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ExpertSystem',
    'south',
    'imagekit'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'ES.urls'

WSGI_APPLICATION = 'ES.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'es',
        'USER': 'es',
        'PASSWORD': 'es',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR,  'templates'),
    os.path.join(BASE_DIR,  'templates/add_system'),
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader', )

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
)

QUERIES_DEBUG = False

MEDIA_ROOT = os.path.join(_PATH, 'media')
MEDIA_URL = '/media/'

DEPLOY_ROOT = "/var/www/projects/rat-expert/"

LOG_FILE = os.path.join(_PATH, PROJECT_NAME + ".log")
if DEPLOY:
    DEPLOY_LOG_ADDRESS = "/serega/special/rat/folder/"  # TODO: if SEREGA: change
    DEBUG = False
    TEMPLATE_DEBUG = True
    ALLOWED_HOSTS = ['*']
    MEDIA_ROOT = DEPLOY_ROOT + "media"
    MEDIA_URL = '/media'

    STATIC_ROOT = DEPLOY_ROOT + "static"
    STATIC_URL = '/static/'

    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'south',
        'ExpertSystem',
        'imagekit'
    )
    LOG_FILE = DEPLOY_LOG_ADDRESS + PROJECT_NAME + ".log"


if not os.path.exists(LOG_FILE):
    try:
        os.makedirs(os.path.dirname(LOG_FILE))
        open(LOG_FILE, 'a').close()
    except OSError as e:
        LOG_FILE = "/dev/null"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'logfile': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': LOG_FILE,
            'maxBytes': 50000,
            'backupCount': 2,
            'formatter': 'standard',
        },
        'console':{
            'level':'INFO',
            'class':'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers':['console'],
            'propagate': True,
            'level':'WARN',
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'ExpertSystem': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
        },
    }
}