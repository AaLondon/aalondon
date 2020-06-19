from django.core.management.base import BaseCommand

import datetime 
from django.utils.timezone import make_aware
from django.conf import settings
from django.utils import timezone
from django.core.mail import send_mail
import requests 
from bs4 import BeautifulSoup 
from meetings.models import Meeting

import calendar
days = dict(zip(calendar.day_name, range(7)));
import os


                

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):

        #TODO get list of intergroup ids of interest

        #iterate over intergroups and import meetings into meeting model

        print('get meetings')
        Meeting.objects.all().delete()

        igs = {117:"City Of London",36:"East London",123:"Chelsea",124:"Chelsea & Fulham",118:"London North East",51:"London North",64:"London North Middlesex",
        63:"London North West",62:"London South Middlesex",119:"London West End",120:"London Westway",75:"London Croydon Epsom & Sutton",55:"London North Kent",
        122:"London South East (East)",121:"London South East (West)",77:"London South",42:"London South West"}    
        for id in igs:
            page = requests.get(f'https://www.alcoholics-anonymous.org.uk/markers.do?ig={id}', verify=False) 
            soup = BeautifulSoup(page.text, 'html.parser') 
            meetings=soup.find_all('marker')
            for meeting in meetings:
                
                
                address = meeting.get('address')
                code = meeting.get('code')
                day = meeting.get('day')
                hearing = meeting.get('hearing')
                lat = meeting.get('lat') or None
                lng = meeting.get('lng') or None
                postcode = meeting.get('postcode')
                slat = meeting.get('slat')
                slng = meeting.get('slng')
                time = meeting.get('time')
                title = meeting.get('title')
                wheelchair = meeting.get('wheelchair')
                intergroup = igs[id]
                time = time.replace(".",":")
                hour = int(time[:2])
                minute = int(time[3:5]) 
                weekday_as_int = days[day]
                time = datetime.time(hour,minute)
                meeting_detail = requests.get(f'https://www.alcoholics-anonymous.org.uk/detail.do?id={code}', verify=False) 
                print(f'https://www.alcoholics-anonymous.org.uk/detail.do?id={code}')

                new_meeting = Meeting.objects.get_or_create(address=address,code=code,day=day,hearing=hearing,lat=lat,\
                day_number=weekday_as_int,lng=lng,postcode=postcode,time=time,title=title,wheelchair=wheelchair,intergroup=intergroup,detail=meeting_detail)
                
                
        day_numbers = [0,1,2,3,4,5,6,7]
        for number in day_numbers:
            meeting = Meeting.objects.filter(day_number=number).order_by('time').first()
            
            if meeting:
                print(meeting)  
                meeting.day_rank = 1
                meeting.save()




