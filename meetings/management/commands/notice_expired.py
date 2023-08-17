from django.core.management.base import BaseCommand
import datetime

from meetings.models import Meeting


class Command(BaseCommand):
    help = 'Update meeting temporary changes...'

    def handle(self, *args, **options):
        today = datetime.datetime.now().date().day
        Meeting.objects.filter(note_expiry_date__day__lt=today).update(
            temporary_changes=None, note_expiry_date=None)
        

