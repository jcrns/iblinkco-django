# Generated by Django 3.0.5 on 2020-05-04 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0015_jobpost_job_fee'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobpost',
            name='job_rating',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
