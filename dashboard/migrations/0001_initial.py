# Generated by Django 4.0.5 on 2022-06-21 15:14

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Farm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('langitude', models.FloatField(blank=True, null=True)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('number_of_trees', models.IntegerField(blank=True, null=True)),
                ('address', models.CharField(blank=True, max_length=20, null=True)),
                ('type', models.CharField(choices=[('NORMAL', 'NORMAL'), ('DEMO', 'DEMO')], default='NORMAL', max_length=20)),
                ('UPI', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Farmer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=20)),
                ('lastname', models.CharField(blank=True, max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Trainer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=20)),
                ('lastname', models.CharField(blank=True, max_length=20)),
                ('institution', models.CharField(blank=True, max_length=20, null=True)),
                ('phonenumber', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='TrainingModule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('GAPName', models.CharField(blank=True, max_length=20, null=True)),
                ('category', models.CharField(blank=True, max_length=20, null=True)),
                ('description', models.TextField(blank=True, max_length=300, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Training',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('langitude', models.FloatField(blank=True, null=True)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('number_of_participants', models.IntegerField()),
                ('country', models.CharField(blank=True, max_length=20, null=True)),
                ('department', models.CharField(blank=True, max_length=20, null=True)),
                ('commune', models.CharField(blank=True, max_length=20, null=True)),
                ('village', models.CharField(blank=True, max_length=20, null=True)),
                ('observation', models.TextField(blank=True, max_length=300, null=True)),
                ('module', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.trainingmodule')),
                ('trainer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.trainer')),
            ],
        ),
        migrations.CreateModel(
            name='FarmVisit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('village', models.CharField(blank=True, max_length=20, null=True)),
                ('observation', models.TextField(blank=True, max_length=300, null=True)),
                ('farm', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.farm')),
            ],
        ),
        migrations.AddField(
            model_name='farm',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.farmer'),
        ),
    ]