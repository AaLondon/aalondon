from rest_framework import serializers
from rest_framework.serializers import (
    ModelSerializer,
    ListSerializer,
    StringRelatedField,
)
from meetings.models import MeetingIntergroup, Meeting, MeetingDay


class MeetingDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingDay
        fields = ["value"]


class MeetingNeufSerializer(serializers.ModelSerializer):
    day = MeetingDaySerializer(many=True)

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
        ]

    def create(self, validated_data):
        days = validated_data.pop("day")
        meeting = MeetingNeuf.objects.create(**validated_data)
        meeting.save()
        for day in days:
            meeting_day, _ = MeetingDay.objects.get_or_create(value=day["value"])
            meeting.day.add(meeting_day)
        return meeting
