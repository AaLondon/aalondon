from django.core.management.base import BaseCommand
from pcndodger.suspensions.models import Address,Suspension
import datetime 
from django.utils.timezone import make_aware
from django.conf import settings
from django.utils import timezone
from django.core.mail import send_mail

from pcndodger.suspensions.mail import get_emails_by_user
                

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):

        get_emails_by_user()

        
       
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days = 1)
        tomorrow = today + datetime.timedelta(days = 1) 
        print('Yesterday : ',yesterday)
        print('Today : ',today)
        print('Tomorrow : ',tomorrow)
        suspensions_less_than_or_equal_tomorrow = Suspension.objects.filter(start_date__date__lte=tomorrow)
        suspensions = suspensions_less_than_or_equal_tomorrow.filter(end_date__date__gte=tomorrow).select_related()
        
        for suspension in suspensions:
            
            if hasattr(suspension.road,'addresses'):
                for address in suspension.road.addresses.all():
                    print(address.user.first_name)
                    print(address.user.last_name)
                    print(suspension.road)
                    print(suspension.reason)
                    print(suspension.location)
                    print(suspension.start_date)
                    print(hasattr(suspension.road,'address_set'))
                    print(address.user.email)
                    body = """ 
Hi %s

You could be caught out by a parking bay suspension tomorrow on %s.

Please move your car this evening if you are affected!!

Here are the details of the suspension:

Location: %s
Reason: %s
Start date: %s
End date: %s
                        
kind regards
Chris Wedgwood
chris@peoplevsparkingtickets.co.uk
 """ %(address.user.first_name,suspension.road,suspension.location,suspension.reason,suspension.start_date.date(),suspension.end_date.date())                           
            
                    print(body)
                    customer_email = send_mail(
                    subject='Suspended Bay Parking Alert from PeopleVsParkingTickets',
                    message=body,
                    from_email='info@peoplevsparkingtickets.co.uk',
                    recipient_list=[address.user.email],
                    fail_silently=False
                  
        )
