from settings import *

DEBUG = False
ALLOWED_HOSTS = ['*']

DEPLOY_ROOT = os.environ("rat_expert_root")

LOG_FILE = os.path.join(DEPLOY_ROOT, "log",  PROJECT_NAME + ".log")

MEDIA_ROOT = os.path.join(DEPLOY_ROOT, "media")
MEDIA_URL = '/media'

STATIC_ROOT = os.path.join(DEPLOY_ROOT, "static")
STATIC_URL = '/static/'

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