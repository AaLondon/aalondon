from django.shortcuts import render
from meetings.models import Meeting
from rest_framework import viewsets
from api.serializers import MeetingSerializer


# Create your views here.

class MeetingViewSet(viewsets.ModelViewSet):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer

