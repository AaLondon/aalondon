# context_processors.py
import environ
from service.models import ServicePage

env = environ.Env()
GA_TRACKING_ID = env('GA_TRACKING_ID',default='None')

def servicepages(request):
    servicepages = ServicePage.objects.all()
    return {
       "servicepages": servicepages,
       "ga_tracking_id": GA_TRACKING_ID 

    }