from .base import *
from .base import env
DEBUG = False



try:
    from .local import *
except ImportError:
    pass


SECRET_KEY = env('DJANGO_SECRET_KEY')
