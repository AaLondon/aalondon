from django.test import TestCase

class TestURLSuccess(TestCase):
    def test_visit_home(self):
        response = self.client.get('/')
        assert response.status_code == 200
    def test_visit_meetings2(self):
        response = self.client.get('/meetings2/')
        print (response)
        # [Tintinnabulate 2020-07-22] XXX:
        # `response.status_code == 404` because meetingslist2 goes nowhere!
        # I think you might mean meetingslist3...
        assert response.status_code == 200
    def test_visit_meetingsearch(self):
        response = self.client.get('/meetingsearch/')
        assert response.status_code == 200
    def test_visit_onlinemeetingsearch(self):
        response = self.client.get('/onlinemeetingsearch/')
        assert response.status_code == 200
    # [Tintinnabulate 2020-07-22] TODO: test rest_framework.urls
