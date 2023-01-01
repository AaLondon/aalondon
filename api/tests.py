from django.test import TestCase
from rest_framework.test import APITestCase

from meetings.tests.factories import MeetingFactory

class TestURLSuccess(TestCase):
    """
    Just test that each api endpoint returns 200
    """
    def test_visit_api_root(self):
        response = self.client.get('/api/')
        assert response.status_code == 200
    def test_visit_meetings(self):
        response = self.client.get('/api/meetings/')
        assert response.status_code == 200
    def test_visit_meetingsearch(self):
        response = self.client.get('/api/meetingsearch/')
        assert response.status_code == 200
    def test_visit_onlinemeetingsearch(self):
        response = self.client.get('/api/onlinemeetingsearch/')
        assert response.status_code == 200
    def test_visit_meetingguide(self):
        response = self.client.get('/api/meetingguide/')
        assert response.status_code == 200
    def test_visit_meetingguide_json(self):
        response = self.client.get('/api/meetingguide.json')
        assert response.status_code == 200


class TestMeetingAPI(APITestCase):

    def setUp(self):
        self.meeting_count = 100
        # create meeting test data.
        for _ in range(self.meeting_count):
            MeetingFactory()
            
        self.api_meetings_url = "/api/meetings/"
    
    def test_api_meetings_count(self):
        response = self.client.get(self.api_meetings_url, format="json") # call `/api/meetings/` api.
        count = response.json()['count'] # get total meetings.
        self.assertEquals(int(count), self.meeting_count)
