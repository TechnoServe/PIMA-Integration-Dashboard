import os
from celery import Celery
#from django.conf import settings
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PIMA_Dashboard.settings')

app = Celery('PIMA_Dashboard')
app.config_from_object('django.conf:settings', namespace='CELERY')


#Celery beat Settings
app.conf.beat_schedule = {
    
    'fetch-programsAndprojects-every-30mins': {
        'task' : 'dashboard.tasks.getProgramsAndProjects',
        'schedule' : crontab(minute='*/30'),
    },

    'fetch-trainingObservations-every-30mins': {
        'task' : 'dashboard.tasks.getTrainingObservations',
        'schedule' : crontab(minute='*/30'),
    },

    'fetch-trainingSessions-every-30mins': {
        'task' : 'dashboard.tasks.getTrainingSessions',
        'schedule' : crontab(minute='*/30'),
    },

    'fetch-demoPlots-every-30mins': {
        'task' : 'dashboard.tasks.getDemoPlots',
        'schedule' : crontab(minute='*/30'),
    },
    
    'fetch-farmVisits-every-30mins': {
        'task' : 'dashboard.tasks.getFarmVisits',
        'schedule' : crontab(minute='*/30'),
    }
}


# Load task modules from all registered Django apps.
app.autodiscover_tasks()

