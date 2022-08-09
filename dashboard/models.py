from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.

class TrainingObservation(models.Model):
    Salesforce_Id =  models.CharField(max_length=30)
    Date_c = models.DateField(blank=True, null=True)
    Project_Name_c =  models.CharField(max_length=50, blank=True, null=True)
    Project_Name_c_slug = models.SlugField()
    Program_c = models.CharField(max_length=50, blank=True, null=True)
    Observation_Location_Latitude_s =  models.FloatField()
    Observation_Location_Longitude_s =  models.FloatField()
    Trainer_c =  models.CharField(max_length=20, null=True, blank=True)
    Number_of_Participants_c = models.IntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.Project_Name_c_slug = slugify(self.Project_Name_c)
        super().save(*args, **kwargs)


class TrainingSession(models.Model):
    Salesforce_Id =  models.CharField(max_length=30)
    Date_c = models.DateField(blank=True, null=True)
    Program_c =  models.CharField(max_length=50, blank=True, null=True)
    Project_Name_c = models.CharField(max_length=50, blank=True, null=True)
    Project_Name_c_slug = models.SlugField()
    Location_GPS_Latitude_s = models.FloatField()
    Location_GPS_Longitude_s = models.FloatField()
    Number_in_Attendance_c = models.IntegerField(blank=True, null=True)
    Training_Group_c = models.CharField(max_length=30,blank=True, null=True)
    Trainer_c = models.CharField(max_length=30, blank=True, null=True)
    Module_Name_c = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.Project_Name_c_slug = slugify(self.Project_Name_c)
        super().save(*args, **kwargs)

class DemoPlot(models.Model):
    Salesforce_Id =  models.CharField(max_length=30)
    Date_c = models.DateField(blank=True, null=True)
    Project_Name_c =  models.CharField(max_length=50, blank=True, null=True)
    Project_Name_c_slug = models.SlugField()
    Program_c = models.CharField(max_length=50, blank=True, null=True)
    Observation_Location_Latitude_s =  models.FloatField()
    Observation_Location_Longitude_s =  models.FloatField()
    Trainer_c =  models.CharField(max_length=20, null=True, blank=True)
    Number_of_Participants_c = models.IntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.Project_Name_c_slug = slugify(self.Project_Name_c)
        super().save(*args, **kwargs)
        
    

class FarmVisit(models.Model):
    pass