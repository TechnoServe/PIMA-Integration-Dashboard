# Generated by Django 4.0.5 on 2022-07-26 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_training_session_c_trainer_c_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='training_session_c',
            old_name='Project_Name_c',
            new_name='Program_c',
        ),
        migrations.AddField(
            model_name='observation_c',
            name='Program_c',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
