import uuid
from django.db import models

# Create your models here.


class Farmer(models.Model):
    firstname =  models.CharField(max_length=20)
    lastname = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f'{self.firstname}'



class Farm(models.Model):

    FARM_TYPE = [
        ("NORMAL", "NORMAL"),
        ("DEMO", "DEMO"),
    ]

    code = models.UUIDField(default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(Farmer, on_delete=models.SET_NULL, null=True)
    latitude = models.FloatField(null=True, blank=True)
    langitude = models.FloatField(null=True, blank=True)
    number_of_trees = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=20, blank=True, null=True)
    type = models.CharField(choices=FARM_TYPE, default="NORMAL", max_length=20)
    UPI = models.CharField(max_length=20, blank=True, null=True)
    #shapefile = models.FileField or models.FilePathField  #To-decide-later

    def __str__(self):
        return f'{self.code}'


class FarmVisit(models.Model):
    date = models.DateField(auto_now_add=True)
    village = models.CharField(max_length=20, blank=True, null=True)
    observation = models.TextField(max_length=300, blank=True, null=True)
    farm = models.ForeignKey(Farm, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return f'{self.date}'




class Trainer(models.Model):
    firstname =  models.CharField(max_length=20)
    lastname = models.CharField(max_length=20, blank=True)
    institution = models.CharField(max_length=20, blank=True, null=True)
    phonenumber = models.CharField(max_length=10)
    email =  models.EmailField()

    def __str__(self) -> str:
        return f'{self.email}'



class TrainingModule(models.Model):
    GAPName =  models.CharField(max_length=20, blank=True, null=True)
    category = models.CharField(max_length=20, blank=True, null=True) #Find the categories and change this field
    description = models.TextField(max_length=300, blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.GAPName}'



class Training(models.Model):
    date = models.DateField(auto_now_add=True)
    latitude = models.FloatField(null=True, blank=True)
    langitude = models.FloatField(null=True, blank=True)
    number_of_participants = models.IntegerField()
    module = models.ForeignKey(TrainingModule, on_delete=models.SET_NULL, blank=True, null=True)
    trainer = models.ForeignKey(Trainer, on_delete=models.SET_NULL, null=True)
    country = models.CharField(max_length=20, blank=True, null=True)
    department =models.CharField(max_length=20, blank=True, null=True)
    commune = models.CharField(max_length=20, blank=True, null=True)
    village = models.CharField(max_length=20, blank=True, null=True)
    observation = models.TextField(max_length=300, blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.date}'