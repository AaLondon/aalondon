from django.shortcuts import render
from meetings.models import Meeting
from rest_framework import viewsets, generics,views
from api.serializers import MeetingSerializer
from datetime import datetime,timedelta
from django.db.models import Q
from django.db.models import IntegerField, Value
from rest_framework.response import Response



# Create your views here.

class MeetingViewSet(viewsets.ModelViewSet):
    queryset = Meeting.objects.all().order_by('time')
    serializer_class = MeetingSerializer



class MeetingsList3(views.APIView):
    

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        serializer = MeetingSerializer(Meeting.objects.all(), many=True)
        print(type(serializer.data))
        meetings = [meeting.title for meeting in Meeting.objects.all()]
        return Response(serializer.data)


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
            date_today = now.date()
            time_now = now.time()
            datetime_now = datetime.combine(date_today,time_now)
            day_name_today = now.strftime("%A")
            tomorrow = now + timedelta(days=1) 
            day_name_tomorrow = tomorrow.strftime("%A")
            
            meetings_today = Meeting.objects.filter((Q(day=day_name_today) & Q(time__gte=now.time())))#.order_by('time')
            meetings_tomorrow = Meeting.objects.filter((Q(day=day_name_tomorrow) & Q(time__lte=now.time())))#.order_by('time')
            

            all = meetings_today | meetings_tomorrow
            if day_name_today == 'sunday':
                all_ordered = all.order_by('-day_number','time')
            else:
                all_ordered = all.order_by('day_number','time')
            return all_ordered
        
        return Meeting.objects.all()

 