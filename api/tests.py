import datetime
import random
from django.test import TestCase
from rest_framework.test import APITestCase
from meetings.models import Meeting


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
        self.meeting_types = ["F2F", "ONL", "HYB"] 
        self.meeting_count = 50

        # create meeting test data.
        for _ in range(self.meeting_count):
            Meeting(
                title=f"Meeting 0{_}",
                time=datetime.time(10,30),
                published=True,
                type=random.choice(self.meeting_types)).save()
        
        # api urls.
        self.api_meetings_url = "/api/meetings/"
        self.api_meetingsearch_url = "/api/meetingsearch/"
    
    def test_api_meetings_count(self):
        response = self.client.get(self.api_meetings_url, format="json") # call `/api/meetings/` api.
        count = int(response.json()['count']) # get total meetings.
        self.assertEquals(count, self.meeting_count)

    def test_api_meetingsearch(self):
        """
            NOTE:
                - test `/api/meetingsearch/` api by searching random meeting
                  titles and types.
        """
        num = random.choice([_ for _ in range(self.meeting_count)])
        test_search = f"Meeting 0{num}"
        meeting_type = random.choice(self.meeting_types) 
        response = self.client.get(
            self.api_meetingsearch_url + f"?search=meeting%200{num}&type={meeting_type}",
            format="json") # call `/api/meetingsearch/` api.
        
        # get returned meeting results.
        meeting_data = response.json()

        # if meeting_count is greater than 0, results were found.
        if int(meeting_data["count"]) > 0:
            # get meeting title and type from json data.
            search_title = meeting_data["results"][0]["title"]
            search_type = meeting_data["results"][0]["type"]

            # test if search returned correct results.
            if (search_title == test_search) and (search_type == meeting_type):
                self.assertEqual(search_title, test_search)
                self.assertEqual(search_type, meeting_type)
        else:
            self.assertEquals(meeting_data["count"], 0)
