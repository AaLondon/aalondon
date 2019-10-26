import scrapy
from bs4 import BeautifulSoup
from django.utils.timezone import make_aware

from urllib.parse import urljoin
import pandas as pd

from pcndodger.suspensions.models import Suspension, Road,Borough
from scrapy.crawler import CrawlerProcess
from urllib.parse import urlsplit, parse_qs

EXTENSIONS = {
    'scrapy.extensions.corestats.CoreStats': None,
}


class MySpider(scrapy.Spider):
    name = 'registers.camden.gov.uk'
    allowed_domains = ['registers.camden.gov.uk']
    start_urls = [
        'https://www.camden.gov.uk/parking-bay-suspensions#feid',

    ]
    custom_settings = {

        'LOG_ENABLED': False
    }

    def parse(self, response):
        print('parsey')
        print(type(response))
        data = response.text

        soup = BeautifulSoup(data, features="lxml")
        table = soup.findAll('table')[1]
        print(table)
        for a in table.find_all('a', href=True):
            url = urljoin(response.url, a['href'])
            print(url)

            zone = a.text
            yield scrapy.Request(url=a['href'], callback=self.parse_zone,meta={'zone': zone})

    def merge_road(self,road,zone_code,borough,zone,suspension_href):
            print('MERGE ROAD:')
            road = road.strip().title()
            bororugh = borough.strip().title()
            borough_obj = Borough.objects.get(value=borough)

            print(f'{road},{zone_code},{borough},{zone},{suspension_href}')
            road_obj, created = Road.objects.get_or_create(value=road,borough=borough_obj)
            print(f'road:{road_obj}')
            road_obj.zone_code = zone_code
            road_obj.zone = zone
            road_obj.suspendion_href = suspension_href
            road_obj.save()
            return road_obj
   



    def parse_zone(self, response):

        data = response.text
        soup = BeautifulSoup(data, features="lxml")
        table = soup.find('table')
        for a in table.find_all('a', href=True):
            url = urljoin(response.url, a['href'])
            
            print(url)
            if url =="javascript:__doPostBack('GridView1','Page$Next')":
                self.data = {}
                self.data['__EVENTTARGET'] = 'GridView1'
                self.data['__EVENTARGUMENT'] = 'Page$Next'
                yield scrapy.FormRequest.from_response(response, method='POST',
                                                        callback=self.parse_zone,
                                                        formdata=self.data,
                                                        meta={'zone_code': zone_code,'zone': zone}
                                                        )
            query = urlsplit(response.url).query
            params = parse_qs(query)
            zone_code = params['cpz'][0]
            zone = response.meta['zone']



            yield scrapy.Request(url=url, callback=self.parse_road, meta={'zone_code': zone_code,'zone': zone})


    def parse_road(self, response):
        data = response.text
        soup = BeautifulSoup(data, features="lxml")
        table = soup.find_all('table')[0]
        zone_code = response.meta['zone_code']
        zone = response.meta['zone']
        print('PARSE ROAD')

        rows = table.find_all('tr')
        pd.set_option('display.max_colwidth', -1)
        df = pd.read_html(str(table), header=0)[0]
        for i, v in df.iterrows():
            reference = v.Reference
            code ='%s-%s' % (zone_code[0:2], zone_code[-1])
            print('code:%s ' % code.upper())
            print('street:%s ' % v.Street)
            

            if v.Street != 'Next':
                road = self.merge_road(road=v.Street,zone_code=code.upper(),borough='Camden',zone=zone,suspension_href=response.request.url)
                start_date = make_aware(pd.to_datetime(v.StartDate))
                end_date = make_aware(pd.to_datetime(v.EndDate))
                reason = v.Reason
                location = v.Location
                print(reference)
                print(road)
                print(start_date)
                print(end_date)
                print(reason)
                print(location)

                suspension, created = Suspension.objects.get_or_create(reference=reference,road=road)
                suspension.start_date = start_date
                suspension.end_date = end_date
                suspension.reason = reason
                suspension.location = location
                suspension.save()





