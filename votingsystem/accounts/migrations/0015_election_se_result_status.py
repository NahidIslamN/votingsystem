# Generated by Django 5.0.3 on 2024-04-19 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_rename_election_start_election_election_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='election',
            name='se_result_status',
            field=models.BooleanField(default=False),
        ),
    ]
