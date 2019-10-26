# Create your tasks here
from __future__ import absolute_import, unicode_literals
import random
from celery import shared_task
from pcndodger.suspensions.models import Road,Suspension
from bs4 import BeautifulSoup
import pandas as pd
import requests
from django.utils.timezone import is_aware, make_aware
from scrapy.crawler import CrawlerProcess
from .spiders import MySpider
from scrapy.utils.log import configure_logging
from twisted.internet import reactor
import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from billiard.context import Process
from multiprocessing import Queue
from django.core.mail import send_mail
import datetime 
from django.utils.timezone import make_aware
from django.conf import settings
from django.utils import timezone

from .mail import get_emails_by_user


@shared_task(name="sum_two_numbers")
def add(x, y):
    return x + y


@shared_task(name="multiply_two_numbers")
def mul(x, y):
    total = x * (y * random.randint(3, 100))
    return total


@shared_task(name="sum_list_numbers")
def xsum(numbers):
    return sum(numbers)


def scrape_roads():
    url = 'https://www.camden.gov.uk/parking-bay-suspensions#feid'
    r = requests.get(url)
    html_doc = r.text
    soup = BeautifulSoup(html_doc, "html.parser")
    table = soup.findAll('table')[1]
    rows = table.find_all('tr')
    pd.set_option('display.max_colwidth', -1)
    df = pd.read_html(str(table))[0]
    df['href'] = [tag['href'] for tag in table.find_all('a')]
    print("ADDING ROADSZ in")
    for zone_index, zone_row in df.iterrows():
        print(zone_row[0], zone_row[1], zone_row[2])
        url = zone_row[2]
        r = requests.get(url)
        html_doc = r.text
        soup = BeautifulSoup(html_doc, "html.parser")
        table = soup.find('table')
        df2 = pd.read_html(str(table), header=0)[0]
        df2['href'] = [tag['href'] for tag in table.find_all('a')]

        road_list = [[zone_row[0], zone_row[1], road_row[0], 'Camden',
                      'http://registers.camden.gov.uk/SuspendedBays/' + road_row['href'].replace(' ', '%20')]
                     for road_index, road_row in df2.iterrows() if pd.notnull(road_row[1]) == False]
        road_df = pd.DataFrame(road_list, columns=['zone_code', 'zone', 'road', 'borough', 'suspension_href'])

        Roads_dict = road_df.to_dict('roads')

        for record in Roads_dict:
            road, created = Road.objects.get_or_create(road=record['road'], zone_code=record['zone_code'],
                                                       borough=record['borough'], zone=record['zone'],\
                                                       suspension_href=record['suspension_href'])
            road.save()


@shared_task(name="scrape_suspensions")
def scrape_suspensions():
    
    def f(q):
        try:
            runner = CrawlerRunner(get_project_settings())
            deferred = runner.crawl(MySpider)
            deferred.addBoth(lambda _: reactor.stop())
            reactor.run()
            q.put(None)
        except Exception as e:
            q.put(e)

    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    result = q.get()
    p.join()

    if result is not None:
        raise result





@shared_task(name="send_email_alerts")
def send_email_alerts():
    '''
    This task gets all addresses with suspensions and sends an email 
    '''
    today = datetime.date.today()
        
    tomorrow = today + datetime.timedelta(days = 1) 
    suspensions_less_than_or_equal_tomorrow = Suspension.objects.filter(start_date__date__lte=tomorrow)
    suspensions = suspensions_less_than_or_equal_tomorrow.filter(end_date__date__gte=tomorrow).select_related()

    user_email_data = get_emails_by_user()
    print(user_email_data)
    if user_email_data:

        for email,user in user_email_data.items():
            print(email)
            print(user)
            body = """Hi %s \n\nYou could be caught out by a parking bay suspension tomorrow on one or more of your addresses.

Please move your car this evening if you are affected!!

Here are the details of suspensions close to your address:

""" % (user['first_name'])


            for suspension in user['suspensions']:

                body = body + """Road: %s
Location: %s
Reason: %s
Start date: %s
End date: %s

""" %(suspension['road'],suspension['location'],suspension['reason'],suspension['start_date'],suspension['end_date'])

            body = body + """kind regards
Chris Wedgwood
chris@peoplevsparkingtickets.co.uk """        
            print(body)
            customer_email = send_mail(
                                    subject='Suspended Bay Parking Alert from PeopleVsParkingTickets',
                                    message=body,
                                    from_email='info@peoplevsparkingtickets.co.uk',
                                    recipient_list=[email],
                                    fail_silently=False

            )

        