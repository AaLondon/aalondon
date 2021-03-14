from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from meetings.models import Meeting,MeetingDay


class MeetingTests(APITestCase):
    def setUp(self):
        pass

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
            "payment_details": "http://127.0.0.1:8000/someurl/",
            "what_three_words": "",
            "description": "adsdsd",
            "notes": "asdsad",
            "sub_types": [{"value": "British Sign Language"}],
        }
        response = self.client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Meeting.objects.count() ==  1
        assert Meeting.objects.get().title == "Monday Big Book Study"

