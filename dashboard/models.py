from re import T
import uuid
from django.db import models

# Create your models here.

# class DemoPlot(models.Model):
#     pass


class Observation_c(models.Model):
    Salesforce_Id =  models.CharField(max_length=30)
    Date_c = models.DateField(blank=True, null=True)
    Project_Name_c =  models.CharField(max_length=20, blank=True, null=True)
    Observation_Location_Latitude_s =  models.FloatField()
    Observation_Location_Longitude_s =  models.FloatField()
    Trainer_c =  models.CharField(max_length=20, null=True, blank=True)
    Number_of_Participants_c = models.IntegerField(blank=True, null=True)

class Training_Session_c(models.Model):
    Salesforce_Id =  models.CharField(max_length=30)
    Date_c = models.DateField(blank=True, null=True)
    Project_Name_c =  models.CharField(max_length=20, blank=True, null=True)
    Location_GPS_Latitude_s = models.FloatField()
    Location_GPS_Longitude_s = models.FloatField()
    Number_in_Attendance_c = models.IntegerField(blank=True, null=True)
    Training_Group_c = models.CharField(max_length=30,blank=True, null=True)
    Trainer_c = models.CharField(max_length=30, blank=True, null=True)
    Module_Name_c = models.CharField(max_length=30, blank=True, null=True)


# class Farmer(models.Model):
#     firstname =  models.CharField(max_length=20)
#     lastname = models.CharField(max_length=20, blank=True)

#     def __str__(self):
#         return f'{self.firstname}'



# class Farm(models.Model):

#     FARM_TYPE = [
#         ("NORMAL", "NORMAL"),
#         ("DEMO", "DEMO"),
#     ]

#     code = models.UUIDField(default=uuid.uuid4, editable=False)
#     owner = models.ForeignKey(Farmer, on_delete=models.SET_NULL, null=True)
#     latitude = models.FloatField(null=True, blank=True)
#     langitude = models.FloatField(null=True, blank=True)
#     number_of_trees = models.IntegerField(null=True, blank=True)
#     address = models.CharField(max_length=20, blank=True, null=True)
#     type = models.CharField(choices=FARM_TYPE, default="NORMAL", max_length=20)
#     UPI = models.CharField(max_length=20, blank=True, null=True)
#     #shapefile = models.FileField or models.FilePathField  #To-decide-later

#     def __str__(self):
#         return f'{self.code}'


# class FarmVisit(models.Model):
#     date = models.DateField(auto_now_add=True)
#     village = models.CharField(max_length=20, blank=True, null=True)
#     observation = models.TextField(max_length=300, blank=True, null=True)
#     farm = models.ForeignKey(Farm, on_delete=models.SET_NULL, null=True)

#     def __str__(self) -> str:
#         return f'{self.date}'




# class Trainer(models.Model):
#     firstname =  models.CharField(max_length=20)
#     lastname = models.CharField(max_length=20, blank=True)
#     institution = models.CharField(max_length=20, blank=True, null=True)
#     phonenumber = models.CharField(max_length=10)
#     email =  models.EmailField()

#     def __str__(self) -> str:
#         return f'{self.email}'



# class TrainingModule(models.Model):
#     GAPName =  models.CharField(max_length=20, blank=True, null=True)
#     category = models.CharField(max_length=20, blank=True, null=True) #Find the categories and change this field
#     description = models.TextField(max_length=300, blank=True, null=True)

#     def __str__(self) -> str:
#         return f'{self.GAPName}'



# class Training(models.Model):
#     date = models.DateField(auto_now_add=True)
#     latitude = models.FloatField(null=True, blank=True)
#     langitude = models.FloatField(null=True, blank=True)
#     number_of_participants = models.IntegerField()
#     module = models.ForeignKey(TrainingModule, on_delete=models.SET_NULL, blank=True, null=True)
#     trainer = models.ForeignKey(Trainer, on_delete=models.SET_NULL, null=True)
#     country = models.CharField(max_length=20, blank=True, null=True)
#     department =models.CharField(max_length=20, blank=True, null=True)
#     commune = models.CharField(max_length=20, blank=True, null=True)
#     village = models.CharField(max_length=20, blank=True, null=True)
#     observation = models.TextField(max_length=300, blank=True, null=True)

#     def __str__(self) -> str:
#         return f'{self.date}'