from django.test import TestCase
from meetings.models import Meeting
from .factories import MeetingFactory,MeetingDayFactory

class MeetingTests(TestCase):
    def test_str(self):
        meeting = MeetingFactory(title="Thursday Big Book")
        assert meeting.__str__() == "Thursday Big Book"

    def test_meeting_day_str(self):
        meeting_day = MeetingDayFactory(value="Monday")
        assert meeting_day.__str__() == "Monday"


