from django.test import TestCase

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
