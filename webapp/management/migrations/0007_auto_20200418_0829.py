# Generated by Django 3.0.5 on 2020-04-18 08:29

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0006_auto_20200418_0707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='managerevaluation',
            name='answer_two_img',
            field=django_resized.forms.ResizedImageField(crop=None, default='default.jpg', force_format=None, keep_meta=True, quality=0, size=[300, 300], upload_to='application_pics'),
        ),
    ]
