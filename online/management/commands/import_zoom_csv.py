from django.core.management.base import BaseCommand
import datetime 
from django.utils.timezone import make_aware
from django.conf import settings
from django.utils import timezone
from django.core.mail import send_mail
import requests 
from bs4 import BeautifulSoup 
from online.models import  OnlineMeeting

import calendar
days = dict(zip(calendar.day_name, range(7)));
import os
import csv
import time
import datetime 
  




                

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):

        OnlineMeeting.objects.all().delete()    
        with open('zoom_file_initial.csv', newline='') as csvfile:
            meetingreader = csv.reader(csvfile, delimiter=',',)
            for row in meetingreader:
                if row:
                    print(row)
                    time_str = row[1]
                    time = datetime.datetime.strptime(time_str, '%H%M').time()
                    

                    if row[2]=='Zoom daily meetings - all times: London':  
                        for day in ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']:
                            day_number = days[day]
                            meeting ,created = OnlineMeeting.objects.get_or_create(title=row[0],time=time,day=day,link=row[3],platform='Zoom',day_number=day_number)
                    else:
                        day = row[2]
                        day_number = days[day]
                        meeting ,created = OnlineMeeting.objects.get_or_create(title=row[0],time=time,day=row[2],link=row[3],platform='Zoom',day_number=day_number)
              