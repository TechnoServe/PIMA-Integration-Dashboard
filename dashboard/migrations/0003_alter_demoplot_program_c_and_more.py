# Generated by Django 4.0.5 on 2022-08-18 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_farmvisit_date_visited_c_farmvisit_farmer_trainer_c_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demoplot',
            name='Program_c',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='demoplot',
            name='Project_Name_c',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='demoplot',
            name='Salesforce_Id',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='demoplot',
            name='Trainer_c',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='farmvisit',
            name='Farmer_Trainer_c',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='farmvisit',
            name='Program_c',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='farmvisit',
            name='Salesforce_Id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='farmvisit',
            name='Training_Group_c',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='trainingobservation',
            name='Program_c',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='trainingobservation',
            name='Project_Name_c',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='trainingobservation',
            name='Salesforce_Id',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='trainingobservation',
            name='Trainer_c',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='trainingsession',
            name='Program_c',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='trainingsession',
            name='Project_Name_c',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='trainingsession',
            name='Salesforce_Id',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='trainingsession',
            name='Trainer_c',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='trainingsession',
            name='Training_Group_c',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
