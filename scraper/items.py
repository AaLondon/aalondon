# -*- coding: utf-8 -*-

 ## items.py
from scrapy_djangoitem import DjangoItem
from meetings.models import Meeting

class MeetingItem(DjangoItem):
    django_model = Meeting
