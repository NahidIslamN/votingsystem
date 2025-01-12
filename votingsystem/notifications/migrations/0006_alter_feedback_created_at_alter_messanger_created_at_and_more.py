# Generated by Django 5.0.3 on 2024-04-20 03:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0005_alter_feedback_created_at_alter_messanger_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='created_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name=datetime.datetime(2024, 4, 20, 3, 57, 57, 980100, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='messanger',
            name='created_at',
            field=models.DateTimeField(verbose_name=datetime.datetime(2024, 4, 20, 3, 57, 57, 980100, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='notifications',
            name='created_at',
            field=models.DateTimeField(verbose_name=datetime.datetime(2024, 4, 20, 3, 57, 57, 980100, tzinfo=datetime.timezone.utc)),
        ),
    ]
