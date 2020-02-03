# context_processors.py
from service.models import ServicePage

def servicepages(request):
    servicepages = ServicePage.objects.all()
    return {
       "servicepages": servicepages
    }