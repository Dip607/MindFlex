# Generated by Django 5.2.3 on 2025-07-11 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_profile_college_id_profile_is_verified_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='tags',
            field=models.TextField(blank=True, help_text="Comma-separated interests like 'music,reading,coding'"),
        ),
    ]
