# context_processors.py
import environ
from service.models import ServicePage
from online.models import OnlinePage
from wagtail.documents.models import Document
from home.models import Reflections 
env = environ.Env()
GA_TRACKING_ID = env('GA_TRACKING_ID',default='None')
from datetime import date

def servicepages(request):
    servicepages = ServicePage.objects.all()
    pdf = Document.objects.filter(title='Insurance.pdf').first()
    onlinepages = OnlinePage.objects.all()
    today = date.today()
    month = today.strftime('%B').upper()
    day = today.day
    reflection = Reflections.objects.get(day=day,month=month)
    pdf_url=''
    if pdf:
       pdf_url = pdf.file.url
           
    return {
       "servicepages": servicepages,
       "onlinepages":onlinepages,
       "ga_tracking_id": GA_TRACKING_ID,
       "pdf_url":  pdf_url,
       "reflection": reflection,
       "today": today

    }
