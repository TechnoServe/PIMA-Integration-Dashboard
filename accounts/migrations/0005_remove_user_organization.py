# Generated by Django 4.0.5 on 2022-08-17 10:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_user_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='organization',
        ),
    ]
