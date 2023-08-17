from rest_framework import serializers
from meetings.models import MeetingIntergroup, Meeting, MeetingDay, MeetingSubType

from django.conf import settings

WHAT_THREE_WORDS_API_KEY = settings.WHAT_THREE_WORDS_API_KEY


class MeetingDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingDay
        fields = ["id", "value"]


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
            "end_time",
            "online_link",
            "online_password",
            "location",
            "address",
            "postcode",
            "tradition_7_details",
            "what_three_words",
            "email",
            "temporary_changes",
            "note_expiry_date",
            "description",
            "notes",
            "sub_types",
            "gso_opt_out",
            "xmas_open",
            "xmas_closed",
            "submission",
        ]

    def create(self, validated_data):
        days = validated_data.pop("days")
        sub_types = validated_data.pop("sub_types")
        what_three_words = validated_data.get("what_three_words", "")
        meeting = Meeting.objects.create(**validated_data)

        meeting.save()
        for day in days:
            meeting_day = MeetingDay.objects.get(value=day["value"])
            meeting.days.add(meeting_day)
        for sub_type in sub_types:
            meeting_sub_type, created = MeetingSubType.objects.get_or_create(value=sub_type["value"])
            meeting.sub_types.add(meeting_sub_type)
        return meeting

    