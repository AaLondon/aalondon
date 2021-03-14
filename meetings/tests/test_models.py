from django.test import TestCase
from .factories import MeetingFactory,MeetingDayFactory
from django.core import mail


  

class MeetingTests(TestCase):
    def setUp(self):
        self.meeting = MeetingFactory(title="Thursday Big Book")
        self.meeting_day = MeetingDayFactory(value="Monday")
        return super().setUp()

    def test_str(self):
        assert self.meeting.__str__() == "Thursday Big Book"

    def test_meeting_day_str(self):
        assert self.meeting_day.__str__() == "Monday"

    def test_send_mail_to_gso(self):
        pass


