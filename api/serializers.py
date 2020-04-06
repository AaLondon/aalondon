from meetings.models import Meeting
from online.models import OnlineMeeting
from rest_framework import serializers
from datetime import datetime,timedelta
from geopy.distance import geodesic     

class MeetingSerializer(serializers.ModelSerializer):
    actual_datetime = serializers.SerializerMethodField()
    friendly_time = serializers.SerializerMethodField()
    postcode_prefix = serializers.SerializerMethodField()
    distance_from_client = serializers.SerializerMethodField()
    class Meta:
        model = Meeting
        fields = ['code','title','time','address','day','actual_datetime','postcode','slug','lat','lng',
                    'day_rank','friendly_time','postcode_prefix','day_number','intergroup','distance_from_client']


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
        print(origin)

        return  round(geodesic(origin, destination).miles,2)


    
class OnlineMeetingSerializer(serializers.ModelSerializer):
    actual_datetime = serializers.SerializerMethodField()
    friendly_time = serializers.SerializerMethodField()
    zoom_password = serializers.SerializerMethodField()
    class Meta:
        model = OnlineMeeting
        fields = ['id','title','time','day','actual_datetime','link','description','slug',
                    'friendly_time','zoom_password','platform']


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
        description = obj.description
        if 'pwd=' in link or 'pwd=' in description or 'password' in description:
            return 1
        return 0

         