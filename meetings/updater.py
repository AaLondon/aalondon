from apscheduler.schedulers.background import BackgroundScheduler
from meetings.jobs import schedule_temporary_meeting_changes

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(schedule_temporary_meeting_changes, 'interval', hours=24)
    scheduler.start()
