# Generated by Django 3.0.5 on 2020-04-19 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0003_auto_20200419_0934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobpost',
            name='manager_payment',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=100),
        ),
        migrations.AlterField(
            model_name='jobpost',
            name='paid_for',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='jobpost',
            name='price_paid',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=100),
        ),
    ]