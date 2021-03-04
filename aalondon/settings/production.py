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
ALLOWED_HOSTS = ['aa-london.com','www.aa-london.com','alcoholicsanonymouslondon.com','www.alcoholicsanonymouslondon.com',] 

############################################
AWS_ACCESS_KEY_ID = env('DJANGO_DO_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('DJANGO_DO_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('DJANGO_DO_STORAGE_BUCKET_NAME')
AWS_S3_ENDPOINT_URL = 'https://fra1.digitaloceanspaces.com' 
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'aalondon'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
###########################################




# Configure file storage settings 
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_S3_MEDIA_LOCATION = 'aalondon/media'

# MEDIA

MEDIA_URL = f'https://{AWS_S3_ENDPOINT_URL}/{AWS_S3_MEDIA_LOCATION}/'



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

