# Generated by Django 5.0.3 on 2024-04-23 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_election_forget_pass_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='election',
            name='forget_pass_status',
        ),
        migrations.AddField(
            model_name='customuser',
            name='forget_pass_status',
            field=models.BooleanField(default=False),
        ),
    ]
