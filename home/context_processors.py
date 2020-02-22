# context_processors.py
import environ
from service.models import ServicePage
from wagtail.documents.models import Document
env = environ.Env()
GA_TRACKING_ID = env('GA_TRACKING_ID',default='None')

def servicepages(request):
    servicepages = ServicePage.objects.all()
    pdf = Document.objects.filter(title='Insurance.pdf').first()
   
           
    return {
       "servicepages": servicepages,
       "ga_tracking_id": GA_TRACKING_ID,
       "pdf_url": pdf.url

    }