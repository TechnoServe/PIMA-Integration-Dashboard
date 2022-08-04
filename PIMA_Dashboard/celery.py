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
    'fetch-salesforce-trainingObservations-every-60mins': {
        'task' : 'dashboard.tasks.getTrainingObservations',
        'schedule' : crontab(minute='*/10'),
    },
    'fetch-programsAndprojects-from-salesforce': {
        'task' : 'dashboard.tasks.getProgramsAndProjects',
        'schedule' : crontab(minute='*/10'),
    },
    'fetch-salesforce-trainingSessions-every-60mins': {
        'task' : 'dashboard.tasks.getTrainingSessions',
        'schedule' : crontab(minute='*/10'),
    },
    'fetch-demoPlots-every-60mins': {
        'task' : 'dashboard.tasks.getDemoPlot',
        'schedule' : crontab(minute='*/10'),
    }
}


# Load task modules from all registered Django apps.
app.autodiscover_tasks()

