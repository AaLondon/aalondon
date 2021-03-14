from factory import Sequence
from factory.django import DjangoModelFactory 
from meetings.models import Meeting, MeetingDay
import datetime


class MeetingDayFactory(DjangoModelFactory):
    class Meta:
        model = MeetingDay


class MeetingFactory(DjangoModelFactory):
    class Meta:
        model = Meeting

    title = Sequence(lambda n: "Meeting %03d" % n)
    time =  datetime.time(10,30)
    