# Generated by Django 3.0.5 on 2020-05-06 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0019_auto_20200506_0003'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobpost',
            name='client_job_rating',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
