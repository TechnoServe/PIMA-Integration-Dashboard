from django.contrib import admin

# Register your models here.
from dashboard.models import Farmer, Farm, FarmVisit
from dashboard.models import Trainer, TrainingModule, Training

admin.site.register(Farmer)
admin.site.register(Farm)
admin.site.register(FarmVisit)
admin.site.register(Trainer)
admin.site.register(TrainingModule)
admin.site.register(Training)
