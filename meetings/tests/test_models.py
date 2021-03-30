from django.core import mail
from django.test import TestCase
from .factories import MeetingFactory,MeetingDayFactory
from unittest.mock import Mock, patch
from meetings.models import Meeting,EmailContact
import datetime 



class EmailContactTests(TestCase):
    def test_email_contact_str(self):
        contact = EmailContact.objects.create(
            first_name="Gary",
            last_name="Player",
            organisation="GSO",
            email="gary@player.com",
            update_to_gso = True 
        )
        assert contact.__str__() == "Gary Player GSO"
  

class MeetingTests(TestCase):
    def setUp(self):
        self.meeting = MeetingFactory(title="Thursday Big Book",what_three_words="bish.bang.bong")
        self.meeting_day = MeetingDayFactory(value="Monday")
        self.published_meeting = MeetingFactory(published=True)
        self.unpublished_meeting = MeetingFactory(title="unpublished",published=False,email='billw@meeting.com')
        self.new_meeting = MeetingFactory(title="new",submission="new")
        self.existing_meeting = MeetingFactory(title="existing",submission="existing")
        
        EmailContact.objects.create(
            first_name="Homer",
            last_name="Simpson",
            email="homerjsimpson@gso.com",
            organisation="GSO",
            update_to_gso=True

        )

        EmailContact.objects.create(
            first_name="Marge",
            last_name="Simpson",
            email="margesimpson@gso.com",
            organisation="GSO",
            update_to_gso=True

        )

        return super().setUp()

    def test_str(self):
        assert self.meeting.__str__() == "Thursday Big Book"

    def test_meeting_day_str(self):
        assert self.meeting_day.__str__() == "Monday"

    def test_send_mail_to_gso(self):
        pass
    @patch('what3words.Geocoder.convert_to_coordinates')
    def test_what_three_words_returns_lng_lat(self,mock_convert_to_coordinates):
        mock_convert_to_coordinates.return_value ={"coordinates":{"lng":-0.195521,"lat":51.520847}}
        meeting = Meeting.objects.get(title="Thursday Big Book")
        meeting.published =True
        meeting.save()
        assert meeting.lng == -0.195521
        assert meeting.lat == 51.520847

    @patch('what3words.Geocoder.convert_to_coordinates')
    def test_what_three_words_not_called_if_empty(self,mock_convert_to_coordinates):
        mock_convert_to_coordinates.return_value ={"coordinates":{"lng":-0.195521,"lat":51.520847}}
        meeting = MeetingFactory(what_three_words="")
        meeting.save()
        assert not meeting.lng
        assert not meeting.lat 

    @patch('what3words.Geocoder.convert_to_coordinates')
    def test_what_three_words_updates_long_lat_when_changed_and_published(self,mock_convert_to_coordinates):
        mock_convert_to_coordinates.return_value ={"coordinates":{"lng":-0.195521,"lat":51.520847}}
        MeetingFactory(what_three_words="one.two.three")
        meeting = Meeting.objects.get(what_three_words="one.two.three")
        meeting.what_three_words = "four.five.six"   
        meeting.published = True   
        meeting.save()
        assert meeting.lng == -0.195521
        assert meeting.lat == 51.520847
        
    def test_meeting_time_bands(self):
        morning_meeting = MeetingFactory(time=datetime.time(10,30))
        afternoon_meeting = MeetingFactory(time=datetime.time(13,30))
        evening_meeting = MeetingFactory(time=datetime.time(19,30))
        
        assert morning_meeting.time_band == "morning"
        assert afternoon_meeting.time_band == "afternoon"
        assert evening_meeting.time_band == "evening"

    
    def test_meeting_email_sent_to_gso_on_save_if_published(self):
        self.published_meeting.gso_opt_in = True
        self.published_meeting.save()
      
        assert len(mail.outbox) == 1, "Outbox is empty"
        assert mail.outbox[0].subject == "Meeting Added/Updated to aa-london.com"
        assert mail.outbox[0].to == ["homerjsimpson@gso.com","margesimpson@gso.com"]

        
    def test_meeting_email_sent_to_user_and_gso_when_publish_goes_false_to_true(self):
        meeting = Meeting.objects.get(title="unpublished")
        meeting.gso_opt_in = True
        meeting.published = True
        meeting.save()

        assert len(mail.outbox) == 2, "Outbox should have two emails and does not"
        assert mail.outbox[0].to == ["homerjsimpson@gso.com","margesimpson@gso.com"]
        assert mail.outbox[1].to == ["billw@meeting.com"]

    
    def test_emails_for_new_meeting_contains_text(self):
        meeting = Meeting.objects.get(title="new")
        meeting.gso_opt_in = True
        meeting.published = True
        meeting.save()

        assert "Here are the details of a new meeting" in mail.outbox[0].body
        assert "Thank you for letting us know about your new meeting details." in mail.outbox[1].body

    def test_emails_for_existing_meeting_contains_text(self):
        meeting = Meeting.objects.get(title="existing")
        meeting.gso_opt_in = True
        meeting.published = True
        meeting.save()

        assert "details of meeting changes" in mail.outbox[0].body
        assert "Thank you for letting us know about the changes to your meeting details." in mail.outbox[1].body
       
    
        



    


