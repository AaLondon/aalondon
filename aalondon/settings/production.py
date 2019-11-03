from .base import *
from .base import env




try:
    from .local import *
except ImportError:
    pass


SECRET_KEY = env('DJANGO_SECRET_KEY')

ALLOWED_HOSTS = ['206.189.30.197'] 

DEBUG = False
