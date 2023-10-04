import datetime 
from meetings.models import Meeting


def schedule_temporary_meeting_changes():
    today = datetime.datetime.now().date()
    Meeting.objects.filter(
        note_expiry_date__lt=today).update(
        temporary_changes="", note_expiry_date=None)