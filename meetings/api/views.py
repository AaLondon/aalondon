from django.contrib.auth.models import User
from meetings.models import Meeting,EmailContact
from meetings.api.serializers import MeetingSerializer
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core import mail


class MeetingList(generics.ListCreateAPIView):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer

    def _send_mail_to_wagtail_moderators(self,data):
        moderators = User.objects.filter(groups__name="Moderators")
        title = data['title']
        type = data['type']
        intergroup = data['intergroup']
        days = ",".join([obj['value'] for obj in data['days']])
        time = data['time']
        
       

        if moderators:
            to_emails = [obj.email for obj in moderators]
            mail.send_mail(
                "Meeting Added/Updated to aa-london.com",
                f"Hi\nA new {type} meeting has been added\n{title}\n{days}\n{time}\nPlease review and publish this in wagtail",
                "info@aa-london.com",
                to_emails,
            )


   


class MeetingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer
