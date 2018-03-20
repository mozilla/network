'''
Django settings for networkapi project.

Generated by 'django-admin startproject' using Django 1.10.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
'''

import os
import environ
import dj_database_url

app = environ.Path(__file__) - 1
root = app - 1

# We set defaults for values that aren't security related
# to the least permissive setting. For security related values,
# we rely on it being explicitly set (no default values) so that
# we error out first.
env = environ.Env(
    ALLOWED_HOSTS=(list, []),
    ASSET_DOMAIN=(str, ''),
    AWS_LOCATION=(str, ''),
    AWS_SQS_ACCESS_KEY_ID=(str, None),
    AWS_SQS_SECRET_ACCESS_KEY=(str, None),
    AWS_SQS_REGION=(str, None),
    CONTENT_TYPE_NO_SNIFF=bool,
    CORS_REGEX_WHITELIST=(tuple, ()),
    CORS_WHITELIST=(tuple, ()),
    DATABASE_URL=(str, None),
    DEBUG=(bool, False),
    DJANGO_LOG_LEVEL=(str, 'INFO'),
    DOMAIN_REDIRECT_MIDDLWARE_ENABLED=(bool, False),
    ENABLE_WAGTAIL=(bool, False),
    EXECUTE_FAKE_DATA=(bool, False),
    FILEBROWSER_DEBUG=(bool, False),
    FILEBROWSER_DIRECTORY=(str, ''),
    HEROKU_APP_NAME=(str, ''),
    NETWORK_SITE_URL=(str, ''),
    PETITION_SQS_QUEUE_URL=(str, None),
    PULSE_API_DOMAIN=(str, ''),
    PULSE_DOMAIN=(str, ''),
    SET_HSTS=bool,
    SHOW_TAKEOVER=(bool, False),
    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=(str, None),
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=(str, None),
    SSL_REDIRECT=bool,
    TARGET_DOMAIN=(str, None),
    USE_S3=(bool, True),
    USE_X_FORWARDED_HOST=(bool, False),
    XSS_PROTECTION=bool,
)

# Read in the environment
if os.path.exists('../.env') is True:
    environ.Env.read_env('../.env')
else:
    environ.Env.read_env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = root()

APP_DIR = app()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = FILEBROWSER_DEBUG = env('DEBUG')

# This should only be set to True in Heroku review apps
EXECUTE_FAKE_DATA = env('EXECUTE_FAKE_DATA')

# Force permanent redirects to the domain specified in TARGET_DOMAIN
DOMAIN_REDIRECT_MIDDLWARE_ENABLED = env('DOMAIN_REDIRECT_MIDDLWARE_ENABLED')
TARGET_DOMAIN = env('TARGET_DOMAIN')

if env('FILEBROWSER_DEBUG') or DEBUG != env('FILEBROWSER_DEBUG'):
    FILEBROWSER_DEBUG = env('FILEBROWSER_DEBUG')

ALLOWED_HOSTS = env('ALLOWED_HOSTS')
CSRF_TRUSTED_ORIGINS = ALLOWED_HOSTS
ALLOWED_REDIRECT_HOSTS = ALLOWED_HOSTS
USE_X_FORWARDED_HOST = env('USE_X_FORWARDED_HOST')

HEROKU_APP_NAME = env('HEROKU_APP_NAME')

if HEROKU_APP_NAME:
    herokuAppHost = env('HEROKU_APP_NAME') + '.herokuapp.com'
    ALLOWED_HOSTS.append(herokuAppHost)

SITE_ID = 1

ENABLE_WAGTAIL = env('ENABLE_WAGTAIL')

# Use social authentication if there are key/secret values defined
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')
SOCIAL_SIGNIN = SOCIAL_AUTH_GOOGLE_OAUTH2_KEY is not None and \
                    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET is not None

USE_S3 = env('USE_S3')

# Application definition
INSTALLED_APPS = list(filter(None, [

    'filebrowser_s3' if USE_S3 else None,
    'social_django' if SOCIAL_SIGNIN else None,

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.redirects',

    'mezzanine.boot',
    'mezzanine.conf',
    'mezzanine.core',
    'mezzanine.generic',
    'mezzanine.pages',
    'mezzanine.forms',

    'networkapi.wagtailcustomization',

    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites' if ENABLE_WAGTAIL else None,
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search' if ENABLE_WAGTAIL else None,
    'wagtail.admin' if ENABLE_WAGTAIL else None,
    'wagtail.core',
    'wagtail.contrib.modeladmin',
    'wagtail.contrib.styleguide' if ENABLE_WAGTAIL and DEBUG else None,

    'modelcluster',
    'taggit',

    'whitenoise.runserver_nostatic',
    'rest_framework',
    'django_filters',
    'gunicorn',
    'corsheaders',
    'storages',
    'adminsortable',

    # the network site
    'networkapi',
    'networkapi.homepage',
    'networkapi.people',
    'networkapi.news',
    'networkapi.fellows',
    'networkapi.utility',
    'networkapi.landingpage',
    'networkapi.campaign',
    'networkapi.highlights',
    'networkapi.milestones',

    # wagtail-specific "networkapi" data
    'networkapi.minisites',
]))

MIDDLEWARE = list(filter(None, [
    'networkapi.utility.middleware.TargetDomainRedirectMiddleware',

    'mezzanine.core.middleware.UpdateCacheMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'corsheaders.middleware.CorsMiddleware',
    'csp.middleware.CSPMiddleware',


    'mezzanine.core.request.CurrentRequestMiddleware',
    'mezzanine.core.middleware.RedirectFallbackMiddleware',
    'mezzanine.core.middleware.AdminLoginInterfaceSelectorMiddleware',
    'mezzanine.core.middleware.SitePermissionMiddleware',
    'mezzanine.pages.middleware.PageMiddleware',
    'mezzanine.core.middleware.FetchFromCacheMiddleware',

    'wagtail.core.middleware.SiteMiddleware'
    if ENABLE_WAGTAIL else None,
    'wagtail.contrib.redirects.middleware.RedirectMiddleware'
    if ENABLE_WAGTAIL else None,
]))

if SOCIAL_SIGNIN:
    SOCIAL_AUTH_LOGIN_REDIRECT_URL = env(
        'SOCIAL_AUTH_LOGIN_REDIRECT_URL',
        None
    )

    AUTHENTICATION_BACKENDS = [
        'social_core.backends.google.GoogleOAuth2',
        'django.contrib.auth.backends.ModelBackend',
    ]

    # See http://python-social-auth.readthedocs.io/en/latest/pipeline.html
    SOCIAL_AUTH_PIPELINE = (
        'social_core.pipeline.social_auth.social_details',
        'social_core.pipeline.social_auth.social_uid',
        'social_core.pipeline.social_auth.auth_allowed',
        'social_core.pipeline.social_auth.social_user',
        'social_core.pipeline.user.get_username',
        'social_core.pipeline.user.create_user',
        # custom permissions when a user logs on
        'networkapi.utility.userpermissions.set_user_permissions',
        'social_core.pipeline.social_auth.associate_user',
        'social_core.pipeline.social_auth.load_extra_data',
        'social_core.pipeline.user.user_details',
    )

PACKAGE_NAME_FILEBROWSER = 'filebrowser_safe'
PACKAGE_NAME_GRAPPELLI = 'grappelli_safe'

OPTIONAL_APPS = (
    PACKAGE_NAME_FILEBROWSER,
    PACKAGE_NAME_GRAPPELLI,
)

ROOT_URLCONF = 'networkapi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            app('templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': list(filter(None, [
                'social_django.context_processors.backends'
                if SOCIAL_SIGNIN else None,
                'social_django.context_processors.login_redirect'
                if SOCIAL_SIGNIN else None,
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'mezzanine.conf.context_processors.settings',
                'mezzanine.pages.context_processors.page',
            ])),
            'builtins': [
                'mezzanine.template.loader_tags',
            ],
            'libraries': {
                'adminsortable_tags': 'networkapi.utility.templatetags'
                                      '.adminsortable_tags_custom',
                'settings_value': 'networkapi.utility.templatetags'
                                  '.settings_value',
                'mini_site_tags': 'networkapi.minisites.templatetags.mini_site_tags',
            }
        },
    },
]

# network asset domain used in templates
ASSET_DOMAIN = env('ASSET_DOMAIN')

WSGI_APPLICATION = 'networkapi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

DATABASE_URL = env('DATABASE_URL')

if DATABASE_URL is not None:
    DATABASES['default'].update(dj_database_url.config())

DATABASES['default']['ATOMIC_REQUESTS'] = True


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth'
                '.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth'
                '.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth'
                '.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth'
                '.password_validation.NumericPasswordValidator',
    },
]


# Location of root django.contrib.admin URL, use {% url 'admin:index' %}
ADMIN_URL = r'^admin/'

# Remove these classes from the admin interface
ADMIN_REMOVAL = [
    'mezzanine.pages.models.RichTextPage',
    'mezzanine.pages.models.Link',
    'mezzanine.forms.models.Form',
    'mezzanine.generic.models.ThreadedComment',
]

ADMIN_MENU_ORDER = (
    ('Content', ('pages.Page',
                 ('Media Library', 'media-library'))),
    ('Data', (
        'people.Person',
        'news.News',
        'people.InternetHealthIssue',
        'highlights.Highlight',
        'milestones.Milestone'
        )),
    ('Components', ('landingpage.Signup', 'campaign.Petition')),
    ('Site', ('sites.Site', 'redirects.Redirect', 'conf.Setting')),
    ('Users', ('auth.User', 'auth.Group')),
)

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

WHITENOISE_ROOT = app('frontend')
WHITENOISE_INDEX_FILE = True

STATICFILES_DIRS = [
    app('static'),
]

STATICFILES_STORAGE = 'networkapi.utility.staticfiles.NonStrictCompressedManifestStaticFilesStorage'

STATIC_ROOT = root('staticfiles')
WAGTAIL_SITE_NAME = 'Mozilla Foundation'

# Rest Framework Settings
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ],
}

# AWS Credentials (if any)
AWS_SQS_ACCESS_KEY_ID = env('AWS_SQS_ACCESS_KEY_ID')
AWS_SQS_SECRET_ACCESS_KEY = env('AWS_SQS_SECRET_ACCESS_KEY')
AWS_SQS_REGION = env('AWS_SQS_REGION')

# The SQS endpoint where we will send petition signups to
PETITION_SQS_QUEUE_URL = env('PETITION_SQS_QUEUE_URL')

# Storage for user generated files
if USE_S3:
    # Use S3 to store user files if the corresponding environment var is set
    DEFAULT_FILE_STORAGE = 'filebrowser_s3.storage.S3MediaStorage'
    AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_CUSTOM_DOMAIN = env('AWS_S3_CUSTOM_DOMAIN')
    AWS_LOCATION = env('AWS_LOCATION')

    MEDIA_URL = 'https://' + AWS_S3_CUSTOM_DOMAIN + '/'
    MEDIA_ROOT = ''

    FILEBROWSER_DIRECTORY = env('FILEBROWSER_DIRECTORY')

else:
    # Otherwise use the default filesystem storage
    MEDIA_ROOT = root('media/')
    MEDIA_URL = '/media/'

# CORS
CORS_ALLOW_CREDENTIALS = False

if '*' in env('CORS_WHITELIST'):
    CORS_ORIGIN_ALLOW_ALL = True
else:
    CORS_ORIGIN_WHITELIST = env('CORS_WHITELIST')
    CORS_ORIGIN_REGEX_WHITELIST = env('CORS_REGEX_WHITELIST')

# CSP
CSP_DEFAULT = (
    'self',
    'localhost:8000',
)

CSP_DEFAULT_SRC = env('CSP_DEFAULT_SRC', default=CSP_DEFAULT)
CSP_SCRIPT_SRC = env('CSP_SCRIPT_SRC', default=CSP_DEFAULT)
CSP_IMG_SRC = env('CSP_IMG_SRC', default=CSP_DEFAULT)
CSP_OBJECT_SRC = env('CSP_OBJECT_SRC', default=None)
CSP_MEDIA_SRC = env('CSP_MEDIA_SRC', default=None)
CSP_FRAME_SRC = env('CSP_FRAME_SRC', default=None)
CSP_FONT_SRC = env('CSP_FONT_SRC', default=CSP_DEFAULT)
CSP_CONNECT_SRC = env('CSP_CONNECT_SRC', default=None)
CSP_STYLE_SRC = env('CSP_STYLE_SRC', default=CSP_DEFAULT)
CSP_BASE_URI = env('CSP_BASE_URI', default=None)
CSP_CHILD_SRC = env('CSP_CHILD_SRC', default=None)
CSP_FRAME_ANCESTORS = env('CSP_FRAME_ANCESTORS', default=None)
CSP_FORM_ACTION = env('CSP_FORM_ACTION', default=None)
CSP_SANDBOX = env('CSP_SANDBOX', default=None)
CSP_REPORT_URI = env('CSP_REPORT_URI', default=None)
CSP_WORKER_SRC = env('CSP_WORKER_SRC', default=CSP_DEFAULT)

# Security
SECURE_BROWSER_XSS_FILTER = env('XSS_PROTECTION')
SECURE_CONTENT_TYPE_NOSNIFF = env('CONTENT_TYPE_NO_SNIFF')
SECURE_HSTS_INCLUDE_SUBDOMAINS = env('SET_HSTS')
SECURE_HSTS_SECONDS = 60 * 60 * 24 * 31 * 6
SECURE_SSL_REDIRECT = env('SSL_REDIRECT')
# Heroku goes into an infinite redirect loop without this.
# See https://docs.djangoproject.com/en/1.10/ref/settings/#secure-ssl-redirect
if env('SSL_REDIRECT') is True:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

X_FRAME_OPTIONS = env('X_FRAME_OPTIONS')

DJANGO_LOG_LEVEL = env('DJANGO_LOG_LEVEL')

# LOGGING
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '[%(asctime)s] [%(levelname)s] %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'networkapi': {
            'handlers': ['console'],
            'level': DJANGO_LOG_LEVEL,
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console'],
            'level': DJANGO_LOG_LEVEL,
            'propagate': True,
        },
    },
}

# Frontend
FRONTEND = {
    'PULSE_API_DOMAIN': env('PULSE_API_DOMAIN'),
    'PULSE_DOMAIN': env('PULSE_DOMAIN'),
    'NETWORK_SITE_URL': env('NETWORK_SITE_URL'),
    'TARGET_DOMAIN': env('TARGET_DOMAIN'),
    'SHOW_TAKEOVER': env('SHOW_TAKEOVER'),
}

try:
    from mezzanine.utils.conf import set_dynamic_settings
except ImportError:
    pass
else:
    set_dynamic_settings(globals())
