from django.db import models
from meetings.models import Meeting
from wagtail.core.models import Page
from datetime import datetime,timedelta


class HomePage(Page):
    pass

    def get_context(self, request):
        context = super().get_context(request)

        # Add extra variables and return the updated context
        now = datetime.now() 
        day_name_now = now.strftime("%A")
        tomorrow = now + timedelta(days=1) 
        day_name_tomorrow = tomorrow.strftime("%A")
        meetings = Meeting.objects.filter((Q(day=day_name_now) & Q(time__gte=now.time()))|(Q(day=day_name_tomorrow) & Q(time__lte=now.time())))
        context['meetings'] = meetings

        return context
