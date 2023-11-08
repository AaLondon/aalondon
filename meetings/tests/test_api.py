from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from meetings.models import Meeting, MeetingDay,EmailContact
from meetings.tests.factories import MeetingFactory
from django.core import mail
from wagtail.tests.utils import WagtailTestUtils


class MeetingTests(APITestCase,WagtailTestUtils):
    def setUp(self):
        
        self.moderator_one = self.create_user('moderator_one', 'moderatorone@example.com', 'password')
        self.moderator_one.groups.add(Group.objects.get(name='Moderators'))
        self.moderator_two = self.create_user('moderator_two', 'moderatortwo@example.com', 'password')
        self.moderator_two.groups.add(Group.objects.get(name='Moderators'))

    def test_create_meeting(self):
        """
        Ensure we can create a new meeting object.
        """

        url = reverse("meeting-list")
        data = {
            "title": "Monday Big Book Study",
            "type": "ONL",
            "time": "10:30",
            "email": "meeting@email.com",
            "days": [{"value": "Wednesday"}, {"value": "Thursday"}],
            "address": "",
            "postcode": "",
            "online_link": "http://127.0.0.1:8000/someurl/",
            "online_password": "addsd",
            "intergroup": "East London",
            "submission": "new",
            "tradition_7_details": "http://127.0.0.1:8000/someurl/",
            "what_three_words": "",
            "description": "adsdsd",
            "notes": "asdsad",
            "sub_types": [{"value": "British Sign Language"}],
            "temporary_changes": "New changes",
            "note_expiry_date": "2023-12-25"
        }
        response = self.client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Meeting.objects.count() == 1
        assert Meeting.objects.get().title == "Monday Big Book Study"

    def test_send_mail(self):
        # Use Django send_mail function to construct a message
        # Note that you don't have to use this function at all.
        # Any other way of sending an email in Django would work just fine.
        mail.send_mail("Subject", "Message", "from@example.com", ["to@example.com"])

        # Now you can test delivery and email contents
        assert len(mail.outbox) == 1, "Inbox is not empty"
        assert mail.outbox[0].subject == "Subject"
        assert mail.outbox[0].body == "Message"
        assert mail.outbox[0].from_email == "from@example.com"
        assert mail.outbox[0].to == ["to@example.com"]

    def get_meeting_data(self, meeting):
        data = {
            "title": meeting.title,
            "type": meeting.type,
            "time": meeting.time,
            "email": meeting.email,
            "days": [{"value": "Wednesday"}, {"value": "Thursday"}],
            "address": meeting.address,
            "postcode": meeting.postcode,
            "online_link": meeting.online_link,
            "online_password": meeting.online_password,
            "intergroup": meeting.intergroup,
            "submission": meeting.submission,
            "tradition_7_details": meeting.tradition_7_details,
            "what_three_words": meeting.what_three_words,
            "description": meeting.description,
            "notes": meeting.notes,
            "sub_types": [{"value": "British Sign Language"}],
        }
        return data

    

  





