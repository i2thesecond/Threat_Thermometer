# Generated by Django 3.0.8 on 2020-08-13 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('threatthermometer', '0007_auto_20200811_1929'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='term',
            field=models.CharField(default='cybersecurity', max_length=30),
        ),
        migrations.AddField(
            model_name='tweet',
            name='unique',
            field=models.BooleanField(default=True),
        ),
    ]
