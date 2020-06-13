from django.shortcuts import render
from meetings.models import Meeting
from online.models import OnlineMeeting
from rest_framework import viewsets, generics,views
from api.serializers import MeetingSerializer,OnlineMeetingSerializer
from datetime import datetime,timedelta
from django.db.models import Q
from django.db.models import IntegerField, Value
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db.models import Avg, F, Window
from django.db.models.functions import  Rank
from django.utils import timezone
import pytz
from django.contrib.postgres.search import SearchVector

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
            tz = pytz.timezone('Europe/London') 
            now = datetime.datetime.now(tz=tz)   
            
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
    filterset_fields = ['day','intergroup']
    ordering_fields = ['time']
   
        

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
      
        
        #queryset = Meeting.objects.all()
        queryset =  Meeting.objects.annotate(search=SearchVector('postcode', 'detail'),)
        now = self.request.query_params.get('now',None)
        if now == '1':
            
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

            all = meetings_today #| meetings_tomorrow
            if day_name_today == 'sunday':
                all_ordered = all.order_by('-day_number','time')
            else:
                all_ordered = all.order_by('day_number','time')
            return all_ordered#.annotate(the_rank=rank_by_day)



        search = self.request.query_params.get('search', None)
       
        if search is not None:
            queryset = queryset.filter(search=search)
        
        #filter by time band
        #filter by accessibility

        return queryset.order_by('day_number','time')
    

  

class OnlineMeetingSearch(generics.ListAPIView):
    """
    Return a list of all the products that the authenticated
    user has ever purchased, with optional filtering.
    """
    model = Meeting
    serializer_class = OnlineMeetingSerializer
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter, filters.SearchFilter]
    #filterset_fields = ['day',]
    ordering_fields = ['time']
        

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        day = self.request.query_params.get('day',None)
        tz = pytz.timezone('Europe/London') 
        dt_now = datetime.now(tz=tz) - timedelta(minutes=10)    
        day_name_today = dt_now.strftime("%A")
        
        queryset = OnlineMeeting.objects.filter(Q(day=day) | Q(day='All') ).filter(published=True)
        now = self.request.query_params.get('now',None)
        top = int(self.request.query_params.get('top',0))
        if now == '1':
             
            
            date_today = dt_now.date()
            time_now = dt_now.time()
            datetime_now = datetime.combine(date_today,time_now)
            
            tomorrow = dt_now + timedelta(days=1) 
            day_name_tomorrow = tomorrow.strftime("%A")
            
            meetings_today = OnlineMeeting.objects.filter(((Q(day=day_name_today) | Q(day='All'))   & Q(time__gte=dt_now.time())))#.order_by('time')
            meetings_tomorrow = OnlineMeeting.objects.filter((Q(day=day_name_tomorrow) & Q(time__lte=dt_now.time())))#.order_by('time')
            rank_by_day = Window(expression=Rank(),partition_by=F("day"),order_by=F("time").asc())

            all = meetings_today #| meetings_tomorrow
            if day_name_today == 'sunday':
                all_ordered = all.order_by('time')
            else:
                all_ordered = all.order_by('time')
            
            if top:
                all_ordered = all_ordered[:top]
            return all_ordered#.annotate(the_rank=rank_by_day)

        postcode = self.request.query_params.get('search', None)
        

        if postcode is not None:
            queryset = queryset.filter(postcode__istartswith=postcode)
        return queryset.order_by('time')
    

  