# Generated by Django 3.0.5 on 2020-04-19 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0009_auto_20200418_1222'),
    ]

    operations = [
        migrations.AddField(
            model_name='managerevaluation',
            name='evaluation_completed',
            field=models.BooleanField(default=False),
        ),
    ]
