# Generated by Django 5.0.3 on 2024-04-16 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_customuser_user_type_commissioners_election_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
