# Generated by Django 4.0.5 on 2022-07-26 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_rename_project_name_c_training_session_c_program_c_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='training_session_c',
            name='Project_Name_c',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]