# Generated by Django 4.0.5 on 2022-08-11 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DemoPlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Salesforce_Id', models.CharField(max_length=30)),
                ('Date_c', models.DateField(blank=True, null=True)),
                ('Project_Name_c', models.CharField(blank=True, max_length=50, null=True)),
                ('Project_Name_c_slug', models.SlugField()),
                ('Program_c', models.CharField(blank=True, max_length=50, null=True)),
                ('Observation_Location_Latitude_s', models.FloatField()),
                ('Observation_Location_Longitude_s', models.FloatField()),
                ('Trainer_c', models.CharField(blank=True, max_length=20, null=True)),
                ('Number_of_Participants_c', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FarmVisit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='TrainingObservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Salesforce_Id', models.CharField(max_length=30)),
                ('Date_c', models.DateField(blank=True, null=True)),
                ('Project_Name_c', models.CharField(blank=True, max_length=50, null=True)),
                ('Project_Name_c_slug', models.SlugField()),
                ('Program_c', models.CharField(blank=True, max_length=50, null=True)),
                ('Observation_Location_Latitude_s', models.FloatField()),
                ('Observation_Location_Longitude_s', models.FloatField()),
                ('Trainer_c', models.CharField(blank=True, max_length=20, null=True)),
                ('Number_of_Participants_c', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TrainingSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Salesforce_Id', models.CharField(max_length=30)),
                ('Date_c', models.DateField(blank=True, null=True)),
                ('Program_c', models.CharField(blank=True, max_length=50, null=True)),
                ('Project_Name_c', models.CharField(blank=True, max_length=50, null=True)),
                ('Project_Name_c_slug', models.SlugField()),
                ('Location_GPS_Latitude_s', models.FloatField()),
                ('Location_GPS_Longitude_s', models.FloatField()),
                ('Number_in_Attendance_c', models.IntegerField(blank=True, null=True)),
                ('Training_Group_c', models.CharField(blank=True, max_length=30, null=True)),
                ('Trainer_c', models.CharField(blank=True, max_length=30, null=True)),
                ('Module_Name_c', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]
