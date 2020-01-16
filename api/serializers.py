from meetings.models import Meeting
from rest_framework import serializers
from datetime import datetime,timedelta


class MeetingSerializer(serializers.ModelSerializer):
    actual_datetime = serializers.SerializerMethodField()
    friendly_time = serializers.SerializerMethodField()
    postcode_prefix = serializers.SerializerMethodField()
    class Meta:
        model = Meeting
        fields = ['code','title','time','address','day','actual_datetime','postcode','slug','lat','lng','day_rank','friendly_time','postcode_prefix','day_number','intergroup']


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
        time = obj.time.strftime('%H:%M %p')
        return f'{time}' 
    
    def get_postcode_prefix(self,obj):
        return obj.postcode.split(' ')[0]


    