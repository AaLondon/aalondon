from rest_framework import serializers
from meetings.models import MeetingIntergroup, Meeting, MeetingDay,MeetingSubType
import what3words
from django.conf import settings

WHAT_THREE_WORDS_API_KEY = settings.WHAT_THREE_WORDS_API_KEY

class MeetingDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingDay
        fields = ["id","value"]

class MeetingSubTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingSubType
        fields = ["value"]


class MeetingSerializer(serializers.ModelSerializer):
    days = MeetingDaySerializer(many=True)
    sub_types = MeetingSubTypeSerializer(many=True)

    class Meta:
        model = Meeting
        fields = [
            "type",
            "title",
            "intergroup",
            "days",
            "time",
            "online_link",
            "online_password",
            "address",
            "postcode",
            "payment_details",
            "what_three_words",
            "email",
            "description",
            "notes",
            "sub_types"
        ]

    def create(self, validated_data):
        days = validated_data.pop("days")
        sub_types = validated_data.pop("sub_types")
        what_three_words=validated_data['what_three_words']
        meeting = Meeting.objects.create(**validated_data)
        meeting.covid_open_status = True
        geocoder = what3words.Geocoder(WHAT_THREE_WORDS_API_KEY)
        res = geocoder.convert_to_coordinates(what_three_words)
        if 'coordinates' in res:
            meeting.lat = res['coordinates']['lat']
            meeting.lng = res['coordinates']['lng']
        meeting.save()
        for day in days:
            meeting_day = MeetingDay.objects.get(value=day["value"])
            meeting.days.add(meeting_day)
        for sub_type in sub_types:
            if sub_type == 'Location Temporarily Closed':
                meeting.covid_open_status = False
                meeting.save()
            meeting_sub_type = MeetingSubType.objects.get(value=sub_type["value"])
            meeting.sub_types.add(meeting_sub_type)
        return meeting
