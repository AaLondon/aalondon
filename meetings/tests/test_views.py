from home.test import TestCase


class TestMeetingSearchView(TestCase):
    
    def test_get(self):
      
        self.get_check_200("meeting_search")
        assert self.get_context("description") == "Meeting search"
      