# context_processors.py
from service.models import ServicePage

def servicepages(request):
    servicepages = ServicePage.objects.all()
    return {
       "servicepages": servicepages,
       "ga_tracking_id": 'UA-158763652-1'
    }