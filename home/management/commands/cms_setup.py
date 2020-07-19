from django.core.management.base import BaseCommand
import datetime 
from django.utils.timezone import make_aware
from django.conf import settings
from django.utils import timezone
from django.core.mail import send_mail
import requests 
from bs4 import BeautifulSoup 
from online.models import  OnlineMeeting
from event.models import EventType,EventIndexPage,RecurringEventParent,RecurringEventChild
from service.models import ServiceIndexPage, ServicePage
from wagtail.core.models import Page ,Site
from home.models import HomePage
from wagtailmenus.models import MainMenuItem, MainMenu
from modelcluster.fields import ParentalKey


import calendar
days = dict(zip(calendar.day_name, range(7)));
import os
import csv
import time
from django.utils import timezone

  




                

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):

        #create event types
        _, _ = EventType.objects.get_or_create(value='Intergroup')
        _, _ = EventType.objects.get_or_create(value='Workshop')
        _, _ = EventType.objects.get_or_create(value='Region')
        _, _ = EventType.objects.get_or_create(value='Convention')
        site = Site.objects.first()
        event_type = EventType.objects.first()
        home_page = HomePage.objects.first()
        home_page.show_in_menus = True
        home_page.save()
        main_menu , _ = MainMenu.objects.get_or_create(site=site)
        
        event_index = EventIndexPage(intro='Here be the events',title='Events', show_in_menus=True)
        service_index = ServiceIndexPage(intro='Here be the service',title='Service', show_in_menus=True)
        
        
        home_page.add_child(instance=event_index) 
        revision = event_index.save_revision() 
        revision.publish()

        home_page.add_child(instance=service_index) 
        revision = event_index.save_revision() 
        revision.publish()

        now = timezone.now()
        service = ServicePage(body='Phone Service....', title='Phone Service', show_in_menus=True, first_published_at=now, post_date=now)
        service_index.add_child(instance=service)
        revision = service_index.save_revision() 
        revision.publish()


        MainMenuItem.objects.get_or_create(link_page=service_index, menu=main_menu, link_text='Service' )
        MainMenuItem.objects.get_or_create(link_page=event_index, menu=main_menu, link_text='Events' )
        MainMenuItem.objects.get_or_create(link_url='/meetingsearch', menu=main_menu, link_text='Find a Meeting')
        MainMenuItem.objects.get_or_create(link_page=home_page, menu=main_menu)
 
        
        


          
        