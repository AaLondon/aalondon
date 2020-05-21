from .base import *
from .base import env
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration


try:
    from .local import *
except ImportError:
    pass


SECRET_KEY = env('DJANGO_SECRET_KEY')
DEBUG = False
ALLOWED_HOSTS = ['staging.aa-london.com','www.aa-london.com','alcoholicsanonymouslondon.com','www.alcoholicsanonymouslondon.com','staging.aa-london.com']  



# STORAGES
DO_SPACES_ACCESS_KEY_ID = env('DJANGO_DO_ACCESS_KEY_ID')
DO_SPACES_SECRET_ACCESS_KEY = env('DJANGO_DO_SECRET_ACCESS_KEY')
DO_SPACES_SPACE_NAME = env('DJANGO_DO_STORAGE_BUCKET_NAME') 
DO_SPACES_SPACE_FOLDER = 'staging' # recommended: Your project name, e.g: 'blog' 
DO_SPACES_ENDPOINT_URL = 'https://fra1.digitaloceanspaces.com' # must be your Space endpoint url, e.g: 'https://sfo2.digitaloceanspaces.com' 
DO_SPACES_CACHE_MAX_AGE = 86400 
DO_SPACES_DEFAULT_ACL = None#'public-read'

# Set File locations  
#DO_SPACES_STATIC_LOCATION = 'chriswedgwood/static' 
DO_SPACES_MEDIA_LOCATION = 'staging/media'
DO_SPACES_PUBLIC_MEDIA_LOCATION = '{FOLDER}/media/public'.format(FOLDER=DO_SPACES_SPACE_FOLDER) 
DO_SPACES_PRIVATE_MEDIA_LOCATION = '{FOLDER}/media/private'.format(FOLDER=DO_SPACES_SPACE_FOLDER)

# Static files config 
#STATIC_URL = 'https://{ENDPOINT_URL}/{STATIC_LOCATION}/'.format(ENDPOINT_URL=DO_SPACES_ENDPOINT_URL, STATIC_LOCATION=DO_SPACES_STATIC_LOCATION)

# Configure file storage settings 
#STATICFILES_STORAGE = 'storages.backends.do_spaces.DigitalOceanSpacesStaticStorage' 
DEFAULT_FILE_STORAGE = 'storages.backends.do_spaces.DigitalOceanSpacesPublicMediaStorage' 
PRIVATE_FILE_STORAGE = 'storages.backends.do_spaces.DigitalOceanSpacesPrivateMediaStorage'

# MEDIA
# ------------------------------------------------------------------------------
#
# region http://stackoverflow.com/questions/10390244/
#from storages.backends.s3boto3 import S3Boto3Storage  # noqa E402
#StaticRootS3BotoStorage = lambda: S3Boto3Storage(location='static')  # noqa
#MediaRootS3BotoStorage = lambda: S3Boto3Storage(location='media', file_overwrite=False)  # noqa
# endregion

#MEDIA_URL = 
MEDIA_URL = 'https://{ENDPOINT_URL}/{MEDIA_LOCATION}/'.format(ENDPOINT_URL=DO_SPACES_ENDPOINT_URL, MEDIA_LOCATION=DO_SPACES_MEDIA_LOCATION)



# # SECURITY
# # ------------------------------------------------------------------------------
# # https://docs.djangoproject.com/en/dev/ref/settings/#secure-proxy-ssl-header
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
#  https://docs.djangoproject.com/en/dev/ref/settings/#secure-ssl-redirect
SECURE_SSL_REDIRECT = env.bool('DJANGO_SECURE_SSL_REDIRECT', default=True)
# # https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-secure
SESSION_COOKIE_SECURE = False
# # https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
SESSION_COOKIE_HTTPONLY = True
# # https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-secure
CSRF_COOKIE_SECURE = False
# # https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
CSRF_COOKIE_HTTPONLY = False
# https://docs.djangoproject.com/en/dev/topics/security/#ssl-https
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-seconds
# TODO: set this to 60 seconds first and then to 518400 once you prove the former works
SECURE_HSTS_SECONDS = 60
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-include-subdomains
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool('DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS', default=True)
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-preload
SECURE_HSTS_PRELOAD = env.bool('DJANGO_SECURE_HSTS_PRELOAD', default=True)
# https://docs.djangoproject.com/en/dev/ref/middleware/#x-content-type-options-nosniff
SECURE_CONTENT_TYPE_NOSNIFF = env.bool('DJANGO_SECURE_CONTENT_TYPE_NOSNIFF', default=True)
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-browser-xss-filter
SECURE_BROWSER_XSS_FILTER = True
# https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
X_FRAME_OPTIONS = 'DENY'


SENTRY_DSN = env('SENTRY_DSN') 
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],

        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True
    )

