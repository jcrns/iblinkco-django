# Generated by Django 3.0.5 on 2020-04-29 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_profile_stripe_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='description',
            field=models.TextField(default='none', max_length=5000),
        ),
    ]