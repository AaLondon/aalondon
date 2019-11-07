from django.shortcuts import render
from meetings.models import Meeting
from rest_framework import viewsets, generics
from api.serializers import MeetingSerializer
from datetime import datetime,timedelta
from django.db.models import Q
from django.db.models import IntegerField, Value



# Create your views here.

class MeetingViewSet(viewsets.ModelViewSet):
    queryset = Meeting.objects.all().order_by('time')
    serializer_class = MeetingSerializer




class MeetingsList(generics.ListAPIView):
    """
    Return a list of all the products that the authenticated
    user has ever purchased, with optional filtering.
    """
    model = Meeting
    serializer_class = MeetingSerializer
    

    def get_queryset(self):
        twentyfour = self.request.query_params.get('twentyfour',None)
        if twentyfour == '1':
            
            now = datetime.now() 
            day_name_today = now.strftime("%A")
            tomorrow = now + timedelta(days=1) 
            day_name_tomorrow = tomorrow.strftime("%A")
            
            meetings_today = Meeting.objects.filter((Q(day=day_name_today) & Q(time__gte=now.time())))#.order_by('time')
            meetings_today.annotate(mycolumn=Value(1, output_field=IntegerField()))
            meetings_tomorrow = Meeting.objects.filter((Q(day=day_name_tomorrow) & Q(time__lte=now.time())))#.order_by('time')
            meetings_tomorrow.annotate(mycolumn=Value(1, output_field=IntegerField()))

            
            print(meetings_tomorrow)
            print(meetings_today)
            return meetings_tomorrow.union(meetings_today)   
        
        return Meeting.objects.all()
    