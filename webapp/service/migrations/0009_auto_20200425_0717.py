# Generated by Django 3.0.5 on 2020-04-25 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0008_jobpost_job_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobpost',
            name='milestone_four_files',
            field=models.FileField(default='default.jpg', upload_to='milestone_files'),
        ),
        migrations.AddField(
            model_name='jobpost',
            name='milestone_one_files',
            field=models.FileField(default='default.jpg', upload_to='milestone_files'),
        ),
        migrations.AddField(
            model_name='jobpost',
            name='milestone_three_files',
            field=models.FileField(default='default.jpg', upload_to='milestone_files'),
        ),
        migrations.AddField(
            model_name='jobpost',
            name='milestone_two_files',
            field=models.FileField(default='default.jpg', upload_to='milestone_files'),
        ),
    ]