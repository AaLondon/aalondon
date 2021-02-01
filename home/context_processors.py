# context_processors.py
from aalondon.settings.base import WHAT_THREE_WORDS_API_KEY
import environ
from service.models import ServicePage
from online.models import OnlinePage
from wagtail.documents.models import Document
from home.models import Reflections 
env = environ.Env()
GA_TRACKING_ID = env('GA_TRACKING_ID',default=None)
GOOGLE_TAG_MANAGER_ID = env('GOOGLE_TAG_MANAGER_ID',default=None)
WHAT_THREE_WORDS_API_KEY = env('WHAT_THREE_WORDS_API_KEY',default='None')

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
       "today": today,
       "what_three_words_api_key":WHAT_THREE_WORDS_API_KEY,
       "google_tag_manager_id":GOOGLE_TAG_MANAGER_ID

    }
