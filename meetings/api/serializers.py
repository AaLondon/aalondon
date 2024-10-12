import datetime
from email.utils import parsedate_to_datetime
from pickle import TRUE
from rest_framework import serializers
from meetings.models import MeetingIntergroup, Meeting, MeetingDay, MeetingSubType, confirmation_link
from django.core import mail

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
    note_expiry_date = serializers.CharField(allow_blank=True)
    slug = serializers.CharField(max_length=100, required=False)

    class Meta:
        model = Meeting
        fields = [
            "slug",
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
            "submission",
        ]

    def create(self, validated_data):
        days = validated_data.pop("days")
        sub_types = validated_data.pop("sub_types")
        what_three_words = validated_data.get("what_three_words", "")
        note_expiry_date = validated_data.pop("note_expiry_date")
        
        title = validated_data.get("title")
        slug = validated_data.get("slug", "")
        email = validated_data.get("email")

        convert_date = datetime.datetime.strptime(note_expiry_date, "%Y-%m-%d").date() if len(note_expiry_date) > 0 else None
        meeting = None
        if Meeting.objects.filter(slug=slug).exists():
            meeting_pk = Meeting.objects.filter(slug=slug).update(
                **validated_data, email_confirmed="UNCONFIRMED", note_expiry_date=convert_date
            )
            meeting = Meeting.objects.get(slug=slug)
        else:
            meeting = Meeting.objects.create( 
                **validated_data, email_confirmed="UNCONFIRMED", note_expiry_date=convert_date)
            meeting.save()

        for day in days:
            meeting_day = MeetingDay.objects.get(value=day["value"])
            meeting.days.add(meeting_day)
        for sub_type in sub_types:
            meeting_sub_type, created = MeetingSubType.objects.get_or_create(value=sub_type["value"])
            meeting.sub_types.add(meeting_sub_type)

        # mail.send_mail(
        #     f"aa-london.com | {title} Email Confirmation.",
        #     f"Hi\n\nSo that we can publish your meeting please confirm by clicking the link below.\n\n{confirmation_link(meeting.pk, title, self.context.get('request'))}\n\nIn fellowship,\nAA London Website Team",
        #     'info@aa-london.com',
        #     [email]
        # )
        return meeting

    