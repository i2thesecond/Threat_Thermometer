# Generated by Django 3.0.8 on 2020-08-14 17:33

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('threatthermometer', '0009_auto_20200814_0632'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TwitterFrequency',
        ),
        migrations.AddField(
            model_name='thermometerresults',
            name='trending_keywords',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=''),
        ),
    ]