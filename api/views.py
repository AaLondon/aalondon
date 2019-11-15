from django.shortcuts import render
from meetings.models import Meeting
from rest_framework import viewsets, generics,views
from api.serializers import MeetingSerializer
from datetime import datetime,timedelta
from django.db.models import Q
from django.db.models import IntegerField, Value
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db.models import Avg, F, Window
from django.db.models.functions import  Rank

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
            rank_by_day = Window(expression=Rank(),partition_by=F("day"),order_by=F("time").asc())

            all = meetings_today | meetings_tomorrow
            if day_name_today == 'sunday':
                all_ordered = all.order_by('-day_number','time')
            else:
                all_ordered = all.order_by('day_number','time')
            return all_ordered#.annotate(the_rank=rank_by_day)
        
        return Meeting.objects.all()

 


class MeetingSearch(generics.ListAPIView):
    """
    Return a list of all the products that the authenticated
    user has ever purchased, with optional filtering.
    """
    model = Meeting
    serializer_class = MeetingSerializer
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['day']
    ordering_fields = ['time']
        

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Meeting.objects.all()
        postcode = self.request.query_params.get('search', None)
        print(postcode)
        if postcode is not None:
            queryset = queryset.filter(postcode__istartswith=postcode)
        return queryset
    

  