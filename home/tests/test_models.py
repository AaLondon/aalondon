from django.test import TestCase
from home.models import EmailContact


class HomeModelTests(TestCase):
    def test_email_contact_str(self):
        contact = EmailContact.objects.create(
            first_name="Gary",
            last_name="Player",
            organisation="GSO",
            email="gary@player.com",
            update_to_gso = True 
        )
        assert contact.__str__() == "Gary Player GSO"
