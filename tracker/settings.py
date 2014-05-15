"""
Django settings for tracker project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
import dj_database_url
import os

from memcacheify import memcacheify

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'gh!6wp01q)8bl(7bw(u2u0_gt&un=90ei^4gb7wz-ca*^1u(a('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
COMPRESS_ENABLED = False

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']

# Use memcache via MemCachier on heroku, fallback to LocMem cache if MemCachier isn't set up (no environment variables)
CACHES = memcacheify()
# Dummy cache for development
if DEBUG:
    CACHES['default'] = {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'bootstrapform',
    'compressor',
    'django_select2',
    'corsheaders',
    'djangular',

    'core',
    'accounts',
    'example',
    'overview',
    'engagement',
    'visitors',
    'content',
    'monthlychart',
    'website'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'minidetector.Middleware',
    'core.middlewares.XForwardedForMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
)

ROOT_URLCONF = 'tracker.urls'

WSGI_APPLICATION = 'tracker.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
# use sqlite3 in local (development) environments or configure from DATABASE_URL if present (e.g. on heroku)
# WARNING: In databases other than PostgreSQL group by date won't work correctly

DATABASES = {'default':  dj_database_url.config()}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# This is the default value for TEMPLATE_LOADERS, but PyCharm doesn't find templates without manually adding it
TEMPLATE_LOADERS = ('django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader')

# Custom user models with emails rather than usernames
AUTH_USER_MODEL = 'accounts.AnalyticsUser'

#Custom settings
MAX_PAGE_VIEW_DURATION = 30  # Minutes
CORS_ORIGIN_ALLOW_ALL = True

# django_select2, don't add css/js automatically
AUTO_RENDER_SELECT2_STATICS = False
