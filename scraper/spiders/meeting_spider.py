import scrapy
import os
import pandas as pd
from bs4 import BeautifulSoup
import re
import csv
from scraper.items import MeetingItem
from scrapy import Spider
from scrapy.http import FormRequest,Request
from scrapy.utils.response import open_in_browser
import datetime
from meetings.models import Meeting

zoom_pattern = r"https://[\w+?\.]*zoom\.us/j/.+?[\?pwd=\w+?]+\b"
ZOOM_RE = re.compile(zoom_pattern, re.IGNORECASE | re.MULTILINE)
# Match https://zoom.us/j/<ID> URLs in the Description field of a meeting
# scrape




INTERGROUPS = {
        117: "City Of London",
        36: "East London",
        123: "Chelsea",
        124: "Chelsea & Fulham",
        118: "London North East",
        51: "London North",
        64: "London North Middlesex",
        63: "London North West",
        62: "London South Middlesex",
        119: "London West End",
        120: "London Westway",
        75: "London Croydon Epsom & Sutton",
        55: "London North Kent",
        122: "London South East (East)",
        121: "London South East (West)",
        77: "London South",
        42: "London South West"
        } 

MEETING_STATUS_CODES = {"Back Open Again"    : "5",
                        "Online"             : "4",
                        "Temporarily Closed" : "3"}
class AASpider(scrapy.Spider):
    name = 'aameetings'
    intergroup_urls = {x[0]:f'https://www.alcoholics-anonymous.org.uk/markers.do?ig={x[0]}'  for x  in INTERGROUPS.items()}
    member_ids = []
    source_meeting_codes = []
    
    def closed(self, reason):
        Meeting.objects.exclude(code__in=self.source_meeting_codes).delete()
        print("Meeting codes crawled", (self.source_meeting_codes))
        
    def start_requests(self):
        print("Meeting codes before crawl", (Meeting.objects.all().values_list('code')))
        for intergroup_id,url in self.intergroup_urls.items():
            yield Request(url,callback=self.parse,meta={'intergroup_id':intergroup_id})
   
    def parse(self, response):
        """
        Parser for each intergroup.

        For x in intergroups, parse
        https://www.alcoholics-anonymous.org.uk/markers.do?ig={x}
        """

        soup = BeautifulSoup(response.text, 'html.parser') 
        meetings=soup.find_all('marker')
        for meeting in meetings:
      
            marker_address = meeting.get('address')
            marker_code = meeting.get('code')
            
            
        
            if marker_code == '13286':
                marker_title = "Hampstead FARSI speaking به جلسه فارسی زبانان  لندن خوش آمدید."
            else:
                marker_title = meeting.get('title')
       
            marker_day = meeting.get('day')
            hearing = meeting.get('hearing')
            marker_lat = meeting.get('lat') or None
            marker_lng = meeting.get('lng') or None
            marker_postcode = meeting.get('postcode')
            slat = meeting.get('slat')
            slng = meeting.get('slng')
            marker_time = meeting.get('time')
            marker_wheelchair = meeting.get('wheelchair')
            marker_hearing = meeting.get('hearing')
            marker_time = marker_time.replace(".",":")
            marker_url = response.url
            
            marker_meeting_status = meeting.get('ms')

            
                
            hour = int(marker_time[:2])
            minute = int(marker_time[3:5]) 
            meeting_time = datetime.time(hour,minute)
            
            meeting_data = {
                    'code': marker_code,
                    'day': marker_day,
                    'hearing': marker_hearing,
                    'lat': marker_lat,
                    'lng': marker_lng,
                    'postcode': marker_postcode,
                    'time': meeting_time,
                    'duration': '',
                    'title': marker_title,
                    'wheelchair': marker_wheelchair,
                    'intergroup_id': response.meta['intergroup_id'],
                    'intergroup': INTERGROUPS[response.meta['intergroup_id']],
                    'covid_open_status': covid_open_status
                    }
          

            url = f'https://www.alcoholics-anonymous.org.uk/detail.do?id={marker_code}'
            
            #We dont want to scrape online meetings from aa-gb in this scrape
            if marker_meeting_status != MEETING_STATUS_CODES["Online"]:
                self.source_meeting_codes.append(int(marker_code))
                yield Request(url=url,callback=self.get_meeting_detail,meta={'meeting_data':meeting_data})
        

    
    def get_meeting_detail(self,response):
        """
        Called by parse() for each meeting found.

        For y in meeting, for meeting in intergroup, parse
        https://www.alcoholics-anonymous.org.uk/detail.do?id={y}
        """
        meeting_data = response.meta.get('meeting_data')

        data = response.text
        soup = BeautifulSoup(data, features="lxml")
        dpanel = soup.find('div',{"class": "dpanel"})
        table = soup.find('div',{"class": "dpanel"}).find_parent("table")
        header = soup.find('div',{"class": "dpanel"}).findChild("h3")
        detail_url = response.url
        
                   
        lines =  [line for line in dpanel.strings] 

        detail = "\n".join(lines[3:])
        meeting_data['detail'] = detail

        matches = ZOOM_RE.findall(detail)
        meeting_data['conference_url'] = None
        if matches:
            meeting_data['conference_url'] = matches[0]

        # Now build up the `types` field

        types = []

        if meeting_data['conference_url']:
            types.append("ONL") #  Online meeting

        if meeting_data['covid_open_status'] == False:
            types.append("TC") #  Temporary closure

        if "Full wheelchair access" in meeting_data['detail']:
            types.append("X") #  Wheelchair access

        if "Women" in meeting_data['detail']:
            types.append("W") #  Women's meeting
        elif "Men's" in meeting_data['detail'] or "Mens" in meeting_data['detail']:
            types.append("M") #  Men's meeting

        if "Outdoor" in meeting_data['detail']:
            types.append("OUT") #  Outdoor meeting

        meeting_data['types'] = types

        item = MeetingItem(meeting_data)
        yield item
