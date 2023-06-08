from meetings.models import Meeting
from django.db.models import F
from meetings.api.serializers import MeetingDaySerializer, MeetingSubTypeSerializer
from online.models import OnlineMeeting
from rest_framework.reverse import reverse
from rest_framework import serializers
from datetime import datetime, timedelta
import time
from geopy.distance import geodesic


class MeetingSearchSerializer(serializers.ModelSerializer):
    actual_datetime = serializers.SerializerMethodField()
    friendly_time = serializers.SerializerMethodField()
    postcode_prefix = serializers.SerializerMethodField()
    distance_from_client = serializers.SerializerMethodField()
    day_number = serializers.SerializerMethodField()
    code = serializers.SerializerMethodField()
    place = serializers.SerializerMethodField()
    days = MeetingDaySerializer(many=True)
    sub_types = MeetingSubTypeSerializer(many=True)

    class Meta:
        model = Meeting
        fields = [
            "code",
            "title",
            "time",
            "address",
            "days",
            "actual_datetime",
            "postcode",
            "online_link",
            "online_password",
            "tradition_7_details",
            "slug",
            "lat",
            "lng",
            "day_rank",
            "friendly_time",
            "postcode_prefix",
            "day_number",
            "intergroup",
            "distance_from_client",
            "time_band",
            "place",
            "type",
            "description",
            "what_three_words",
            "sub_types",
            "type",
            "xmas_open",
        ]

    def get_actual_datetime(self, obj):
        now = datetime.now()
        date_today = now.date()
        time_now = now.time()
        datetime_now = datetime.combine(date_today, time_now)
        day_name_today = now.strftime("%A")
        date_tomorrow = now + timedelta(days=1)
        day_name_tomorrow = date_tomorrow.strftime("%A")

        if obj.days == day_name_today:
            actual_datetime = datetime.combine(date_today, obj.time)
        elif obj.days == day_name_tomorrow:
            actual_datetime = datetime.combine(date_tomorrow, obj.time)
        else:
            actual_datetime = None
        return actual_datetime

    def get_friendly_time(self, obj):
        time = obj.time.strftime("%H:%M")
        return f"{time}"

    def get_friendly_end_time(self, obj):
        end_time = obj.end_time.strftime("%H:%M")
        return f"{end_time}"

    def get_postcode_prefix(self, obj):
        if obj.postcode:
            return obj.postcode.split(" ")[0]
        return ""

    def get_distance_from_client(self, obj):
        qp = self.context["request"].query_params
        origin = (qp.get("clientLat", 0), qp.get("clientLng", 0))
        destination = (obj.lat, obj.lng)
        return round(geodesic(origin, destination).miles, 2)

    def get_day_number(self, obj):

        return 0  # time.strptime(obj.day, '%A').tm_wday

    def get_code(self, obj):

        return "physical_" + str(obj.id)

    def get_place(self, obj):

        if obj.postcode:
            return obj.postcode.split(" ")[0]
        return ""


class OnlineMeetingSerializer(serializers.ModelSerializer):
    actual_datetime = serializers.SerializerMethodField()
    friendly_time = serializers.SerializerMethodField()
    zoom_password = serializers.SerializerMethodField()
    code = serializers.SerializerMethodField()
    place = serializers.SerializerMethodField()
    day_number = serializers.SerializerMethodField()

    class Meta:
        model = Meeting
        fields = [
            "id",
            "title",
            "time",
            "days",
            "actual_datetime",
            "online_link",
            "description",
            "slug",
            "friendly_time",
            "zoom_password",
            "code",
            "place",
            "day_number",
            "type",
        ]

    def get_actual_datetime(self, obj):
        now = datetime.now()
        date_today = now.date()
        time_now = now.time()
        datetime_now = datetime.combine(date_today, time_now)
        day_name_today = now.strftime("%A")
        date_tomorrow = now + timedelta(days=1)
        day_name_tomorrow = date_tomorrow.strftime("%A")

        if obj.days == day_name_today:
            actual_datetime = datetime.combine(date_today, obj.time)
        elif obj.days == day_name_tomorrow:
            actual_datetime = datetime.combine(date_tomorrow, obj.time)
        else:
            actual_datetime = None
        return actual_datetime

    def get_friendly_time(self, obj):
        time = obj.time.strftime("%H:%M")
        return f"{time}"

    def get_zoom_password(self, obj):

        # link = obj.online_link
        description = obj.description or ""

        return 0

    def get_code(self, obj):

        return "online_" + str(obj.id)

    def get_place(self, obj):

        return "zoom"

    def get_day_number(self, obj):
        # if obj.day == 'All':
        #    return -1
        return -1  # time.strptime(obj.day, '%A').tm_wday


class MeetingGuideSerializer(serializers.ModelSerializer):
    
    name = serializers.SerializerMethodField()
    notes = serializers.SerializerMethodField()
    updated = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    conference_url = serializers.SerializerMethodField()
    conference_url_notes = serializers.SerializerMethodField()
    day = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()
    end_time = serializers.SerializerMethodField()
    timezone = serializers.SerializerMethodField()
    types = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    location_notes = serializers.SerializerMethodField()
    region = serializers.SerializerMethodField()
    group = serializers.SerializerMethodField()
    formatted_address = serializers.SerializerMethodField()
    latitude = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    

    class Meta:
        model = Meeting
        fields = [
            "name",
            "slug",
            "day",
            "time",
            "end_time",
            "timezone",
            "types",
            "notes",
            "conference_url",
            "conference_url_notes",
            "location",
            "location_notes",
            "formatted_address",
            "country", 
            "latitude",
            "longitude",
            "region",
            "updated",
            "group",
            "url"

        ]


    def get_id(self, obj):
        return obj.code

    def get_name(self, obj):
        return obj.title

    def get_notes(self, obj):
        if obj.address and not obj.online_link:
            return obj.description

    def get_updated(self, obj):
        updated = obj.updated.strftime("%Y-%m-%d %H:%M:%S")
        return updated

    def get_location_id(self, obj):

        return ""

    def get_url(self, obj):

        request = self.context.get("request")
        url = reverse("meeting-detail", kwargs={"slug": obj.slug}, request=request)
        return url

    def get_day(self, obj):
        days = [
            "Sunday",
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
        ]
        days_qs = obj.days.all().annotate(days=F("value")).values_list("days", flat=True)
        sorted_days = [ days.index(day) for day in days_qs ]
        sorted_days.sort()
        return sorted_days

    def get_time(self, obj):
        time = obj.time.strftime("%H:%M")
        return f"{time}"

    def get_end_time(self, obj):

        return ""

    def get_time_formatted(self, obj):

        return ""

    def get_conference_phone(self, obj):
        return ""

    def get_types(self, obj):
        return [type.code for type in obj.sub_types.all()]

    def get_location(self, obj):
        return obj.location

    def get_location_notes(self, obj):
        return ""

    def get_region_id(self, obj):
        return ""

    def get_region(self, obj):
        return ""

    def get_sub_region(self, obj):
        return ""

    def get_group_id(self, obj):
        return obj.code

    def get_group(self, obj):
        return obj.title

    def get_district(self, obj):
        return obj.intergroup

    def get_district_id(self, obj):
        return ""

    def get_sub_district(self, obj):
        return ""

    def get_group_notes(self, obj):
        return ""

    def get_website(self, obj):
        return ""

    def get_website_2(self, obj):
        return ""

    def get_conference_url(self, obj):
        return obj.online_link
    
    def get_conference_url_notes(self, obj):
        if obj.online_link: 
            return obj.description

    def get_formatted_address(self, obj):
        return f"{obj.address},London,United Kingdom,{obj.postcode}" 
        
    def get_latitude(self, obj):
        return obj.lat

    def get_longitude(self, obj):
        return obj.lng

    def get_email(self, obj):
        return ""

    def get_phone(self, obj):
        return ""

    def get_mailing_address(self, obj):
        return ""

    def get_venmo(self, obj):
        return ""

    def get_square(self, obj):
        return ""

    def get_paypal(self, obj):
        return ""

    def get_last_contact(self, obj):
        return ""

    def get_postal_code(self, obj):
        if "online" in obj.title.lower():
            return ""
        return obj.postcode

    def get_city(self, obj):
        return "London"

    def get_state(self, obj):
        return "London"

    def get_country(self, obj):
        return "UK"

    def get_timezone(self, obj):
        return "Europe/London"
