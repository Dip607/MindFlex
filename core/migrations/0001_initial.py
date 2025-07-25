# Generated by Django 5.2.3 on 2025-07-09 09:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(max_length=10)),
                ('city', models.CharField(max_length=50)),
                ('budget', models.IntegerField()),
                ('cleanliness', models.IntegerField()),
                ('sleep_schedule', models.CharField(max_length=20)),
                ('introvert_extrovert', models.CharField(max_length=20)),
                ('bio', models.TextField()),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='profile_pics/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
