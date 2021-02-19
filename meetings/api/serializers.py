from rest_framework import serializers
from rest_framework.serializers import (
    ModelSerializer,
    ListSerializer,
    StringRelatedField,
)
from meetings.models import MeetingIntergroup, Meeting, MeetingDay,MeetingSubType


class MeetingDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingDay
        fields = ["value"]

class MeetingSubTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingSubType
        fields = ["value"]


class MeetingNeufSerializer(serializers.ModelSerializer):
    day = MeetingDaySerializer(many=True)
    sub_types = MeetingSubTypeSerializer(many=True)

    class Meta:
        model = Meeting
        fields = [
            "type",
            "title",
            "intergroup",
            "day",
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
        days = validated_data.pop("day")
        sub_types = validated_data.pop("sub_types")
        meeting = Meeting.objects.create(**validated_data)
        meeting.save()
        for day in days:
            meeting_day, _ = MeetingDay.objects.get(value=day["value"])
            meeting.days.add(meeting_day)
        for sub_type in sub_types:
            meeting_sub_type,_ = MeetingSubType.objects.get(value=sub_type["value"])
            meeting.sub_types.add(meeting_sub_type)
        return meeting
