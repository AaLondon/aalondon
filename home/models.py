from django.db import models
from meetings.models import Meeting
from wagtail.core.models import Page
from datetime import datetime,timedelta
from django.db.models import Q


class HomePage(Page):
    pass

    def get_context(self, request):
        context = super().get_context(request)

        # Add extra variables and return the updated context
        now = datetime.now() 
        day_name_today = now.strftime("%A")
        tomorrow = now + timedelta(days=1) 
        day_name_tomorrow = tomorrow.strftime("%A")
        #meetings = Meeting.objects.filter((Q(day=day_name_now) & Q(time__gte=now.time()))|(Q(day=day_name_tomorrow) & Q(time__lte=now.time())))
        
        meetings_today = Meeting.objects.filter((Q(day=day_name_today) & Q(time__gte=now.time()))).order_by('time')
        meetings_tomorrow = Meeting.objects.filter((Q(day=day_name_tomorrow) & Q(time__lte=now.time()))).order_by('time')
        
        context['meetings_today'] = meetings_today 
        context['meetings_tomorrow'] = meetings_tomorrow 
        context['day_name_tomorrow'] = day_name_tomorrow
        context['day_name_today'] = day_name_today


        return context
