from meetings.models import Meeting
from online.models import OnlineMeeting
from rest_framework import serializers
from datetime import datetime,timedelta
import time
from geopy.distance import geodesic     

class MeetingSerializer(serializers.ModelSerializer):
    actual_datetime = serializers.SerializerMethodField()
    friendly_time = serializers.SerializerMethodField()
    postcode_prefix = serializers.SerializerMethodField()
    distance_from_client = serializers.SerializerMethodField()
    day_number = serializers.SerializerMethodField()
    covid_open_status = serializers.SerializerMethodField()
    code = serializers.SerializerMethodField()
    place = serializers.SerializerMethodField()
  
   
    class Meta:
        model = Meeting
        fields = ['code','title','time','address','day','actual_datetime','postcode','slug','lat','lng',
                    'day_rank','friendly_time','postcode_prefix','day_number','intergroup','distance_from_client','time_band','covid_open_status','place','meeting_type']


    def get_actual_datetime(self, obj):
        now = datetime.now() 
        date_today = now.date()
        time_now = now.time()
        datetime_now = datetime.combine(date_today,time_now)
        day_name_today = now.strftime("%A")
        date_tomorrow = now + timedelta(days=1) 
        day_name_tomorrow = date_tomorrow.strftime("%A")

        if obj.day == day_name_today:
            actual_datetime = datetime.combine(date_today,obj.time)
        elif obj.day == day_name_tomorrow:
            actual_datetime = datetime.combine(date_tomorrow,obj.time)
        else:
            actual_datetime = None
        return actual_datetime
    
    def get_friendly_time(self,obj):
        time = obj.time.strftime('%H:%M')
        return f'{time}' 
    
    def get_postcode_prefix(self,obj):
        return obj.postcode.split(' ')[0]

    def get_distance_from_client(self,obj):
        qp = self.context['request'].query_params
        origin = (qp.get('clientLat',0),qp.get('clientLng',0))
        destination = (obj.lat,obj.lng)
        return  round(geodesic(origin, destination).miles,2)


    def get_day_number(self,obj):
     
        return  time.strptime(obj.day, '%A').tm_wday

    def get_covid_open_status(self,obj):

        if obj.covid_open_status:
            return 1
        else:
            return 0
        
    def get_code(self, obj):

        return 'physical_'+str(obj.id)

    def get_place(self,obj):

        return obj.postcode.split(' ')[0]
        
   


    
class OnlineMeetingSerializer(serializers.ModelSerializer):
    actual_datetime = serializers.SerializerMethodField()
    friendly_time = serializers.SerializerMethodField()
    zoom_password = serializers.SerializerMethodField()
    code = serializers.SerializerMethodField()
    place = serializers.SerializerMethodField()
    day_number = serializers.SerializerMethodField()
  
    class Meta:
        model = OnlineMeeting
        fields = ['id','title','time','day','actual_datetime','link','description','slug',
                    'friendly_time','zoom_password','platform','code','place','day_number']


    def get_actual_datetime(self, obj):
        now = datetime.now() 
        date_today = now.date()
        time_now = now.time()
        datetime_now = datetime.combine(date_today,time_now)
        day_name_today = now.strftime("%A")
        date_tomorrow = now + timedelta(days=1) 
        day_name_tomorrow = date_tomorrow.strftime("%A")

        if obj.day == day_name_today:
            actual_datetime = datetime.combine(date_today,obj.time)
        elif obj.day == day_name_tomorrow:
            actual_datetime = datetime.combine(date_tomorrow,obj.time)
        else:
            actual_datetime = None
        return actual_datetime
    
    def get_friendly_time(self,obj):
        time = obj.time.strftime('%H:%M')
        return f'{time}'

    def get_zoom_password(self,obj):

        link = obj.link
        description = obj.description or ''
        
        return 0

         
    def get_code(self, obj):

        return 'online_'+str(obj.id)


    def get_place(self, obj):

        return 'zoom'

    def get_day_number(self,obj):
        if obj.day == 'All':
            return -1
        return  time.strptime(obj.day, '%A').tm_wday


class MeetingGuideSerializer(serializers.ModelSerializer):

    class Meta:
        model = Meeting
        fields = '__all__'
