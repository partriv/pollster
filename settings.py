# Django settings for pollster project.
from pollster.conf import settings_local
from pollster.consts import consts

DEBUG = settings_local.DEBUG
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

ALLOWED_HOSTS='*'




#'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASES = {
    'default': {
                'ENGINE':'django.db.backends.mysql',
        
        'NAME': settings_local.DATABASE_NAME,                      # Or path to database file if using sqlite3.
        'USER': settings_local.DATABASE_USER,                      # Not used with sqlite3.
        'PASSWORD': settings_local.DATABASE_PASSWORD,                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}
#

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = settings_local.MEDIA_ROOT

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = settings_local.MEDIA_URL

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
   'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'pollster.exception.handler.middleware',
#    'facebook.djangofb.FacebookMiddleware',
)

ROOT_URLCONF = 'pollster.urls'

TEMPLATE_DIRS = settings_local.TEMPLATE_DIRS

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.comments',
    
    'pollster',    
    'threadedcomments',        
)


if settings_local.USE_DJANGO_TOOL_BAR:
    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    INSTALLED_APPS += ('debug_toolbar',)
    INTERNAL_IPS = ('127.0.0.1',)

TEMPLATE_CONTEXT_PROCESSORS = ("django.core.context_processors.auth",)

AUTH_PROFILE_MODEL = 'pollster.UserProfile'

# Comm
APPEND_SLASH = True
LOGIN_URL = "/login/"

EMAIL_HOST = settings_local.EMAIL_HOST
EMAIL_PORT = settings_local.EMAIL_PORT
#EMAIL_HOST_USER = settings_local.EMAIL_HOST_USER
#EMAIL_HOST_PASSWORD = settings_local.EMAIL_HOST_PASSWORD

SESSION_COOKIE_DOMAIN = settings_local.COOKIE_DOMAIN
SESSION_COOKIE_NAME = "strucksession"
SESSION_COOKIE_AGE = 157784630



