from .base import *

ALLOWED_HOSTS = ['13.124.229.142']
STATIC_ROOT = BASE_DIR / 'static/'
STATICFILES_DIRS = []
DEBUG = False
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sbclc',
        'USER': 'dbmasteruser',
        'PASSWORD': '98,RC_xKQ$}&M8R-SRrtb>+2}SMy8WsJ',
        'HOST': 'ls-2e3ea7b61c9294d9ec721d280147ece70acd1208.calkbqcnylxq.ap-northeast-2.rds.amazonaws.com',
        'PORT': '5432',
    }
}
