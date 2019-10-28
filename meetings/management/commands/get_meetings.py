from django.core.management.base import BaseCommand

import datetime 
from django.utils.timezone import make_aware
from django.conf import settings
from django.utils import timezone
from django.core.mail import send_mail
import requests 
from bs4 import BeautifulSoup 
from meetings.models import Meeting


                

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):

        #TODO get list of intergroup ids of interest

        #iterate over intergroups and import meetings into meeting model

        print('get meetings')
        page = requests.get('https://www.alcoholics-anonymous.org.uk/markers.do?ig=23') 
        soup = BeautifulSoup(page.text, 'html.parser') 
        meetings=soup.find_all('marker')
        for meeting in meetings:
            
            
            address = meeting.get('address')
            code = meeting.get('code')
            day = meeting.get('day')
            hearing = meeting.get('hearing')
            lat = meeting.get('lat')
            lng = meeting.get('lng')
            postcode = meeting.get('postcode')
            slat = meeting.get('slat')
            slng = meeting.get('slng')
            time = meeting.get('time')
            title = meeting.get('title')
            wheelchair = meeting.get('wheelchair')
            
            time = time.replace(".",":")
            new_meeting = Meeting.objects.get_or_create(address=address,code=code,day=day,hearing=hearing,lat=lat,lng=lng,postcode=postcode,time=time,title=title,wheelchair=wheelchair)


