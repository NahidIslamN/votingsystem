# Generated by Django 5.0.3 on 2024-04-19 10:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_canditats_discription_canditats_mul_niti'),
    ]

    operations = [
        migrations.RenameField(
            model_name='election',
            old_name='Election_Start',
            new_name='Election_Date',
        ),
        migrations.AddField(
            model_name='election',
            name='elections_start_at',
            field=models.TimeField(default=datetime.time(8, 0)),
        ),
        migrations.AlterField(
            model_name='election',
            name='election_end',
            field=models.TimeField(default=datetime.time(17, 0)),
        ),
    ]
