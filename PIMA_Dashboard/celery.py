import os
from celery import Celery
#from django.conf import settings
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PIMA_Dashboard.settings')

app = Celery('PIMA_Dashboard')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')




#Celery beat Settings
app.conf.beat_schedule = {
    'pull-salesforce-data-every-10mins': {
        'task' : 'dashboard.tasks.getObservations',
        'schedule' : crontab(minute='*/10'),
    },
    'pull-programs-from-salesforce': {
        'task' : 'dashboard.tasks.getPrograms',
        'schedule' : crontab(minute='*/10'),
    }
}


# Load task modules from all registered Django apps.
app.autodiscover_tasks()

