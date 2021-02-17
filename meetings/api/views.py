
from meetings.models import Meeting
from meetings.api.serializers import MeetingNeufSerializer
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

class MeetingNeufList(generics.ListCreateAPIView):
    queryset = Meeting.objects.all()
    serializer_class = MeetingNeufSerializer



class MeetingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Meeting.objects.all()
    serializer_class = MeetingNeufSerializer


