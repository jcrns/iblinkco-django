# Generated by Django 3.0.5 on 2020-04-16 19:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ManagerEvaluation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('evaluation_started', models.BooleanField(default=False)),
                ('answer_one', models.TextField(default='none', max_length=350)),
                ('answer_two', models.TextField(default='none', max_length=350)),
                ('answer_img', models.ImageField(default='default.jpg', null=True, upload_to='application_pics')),
                ('answer_three', models.TextField(default='none', max_length=280)),
                ('choose_job', models.BooleanField(default=False)),
                ('manager', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
