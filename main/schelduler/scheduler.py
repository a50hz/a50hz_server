from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django.utils import timezone
from django_apscheduler.models import DjangoJobExecution
import sys
from apscheduler.triggers.cron import CronTrigger
from script import update


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    # run this job every 24 hours
    scheduler.add_job(
        update,
        trigger=CronTrigger(
            day_of_week="*", hour="00", minute="00"
        ),  # Midnight on Monday, before start of the next work week.
        id="delete_old_job_executions",
        max_instances=1,
        replace_existing=True,
        misfire_grace_time=None,
    )
    register_events(scheduler)
    scheduler.start()
    print("Scheduler started...", file=sys.stdout)