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
import csv



                

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):

            with open('zoom_file.csv', mode='w') as zoom_file:

                page = requests.get(f'https://alcoholicsanonymouslondon.com/online/zoom-meetings/', verify=False) 
                soup = BeautifulSoup(page.text, 'html.parser') 
                meetings=soup.find_all('p')
                day_of_week = ''
                for paragraph in meetings:
            
                    print(paragraph)
                    print()
                    #time = paragraph[0:3]
                    # 
                    time=''
                    if len(paragraph.text) > 5:
                        time = paragraph.text[0:5].strip()
                    
                    if paragraph.findAll('b'):
                        if title in ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday','Zoom daily meetings']:
                            day_of_week = title
                        title = paragraph.findAll('b')[0].text.strip()
                    else:
                        title = 'None'

                    link = ''
                    if paragraph.findAll('a'):
                        link = paragraph.findAll('a')[0].get('href')


                    print(f'title:{title}')
                    print(f'time:{time}')
                    print(f'day:{day_of_week}')
                    print(f'link:{link}')
                
                    zoom_writer = csv.writer(zoom_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    zoom_writer.writerow([title, time, day_of_week,link])
               
