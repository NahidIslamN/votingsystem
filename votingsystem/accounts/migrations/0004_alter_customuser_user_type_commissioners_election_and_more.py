# Generated by Django 5.0.3 on 2024-04-16 09:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_customuser_mobile_alter_customuser_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[(1, 'ENIC'), (2, 'NIC'), (3, 'Canditats'), (4, 'Observer'), (5, 'Voter')], max_length=50),
        ),
        migrations.CreateModel(
            name='Commissioners',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comitionar_ID', models.CharField(max_length=10, unique=True)),
                ('Zone_Name', models.CharField(max_length=25)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_ad', models.DateTimeField(auto_now=True)),
                ('users', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Election',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_ad', models.DateTimeField(auto_now=True)),
                ('Election_Start', models.DateTimeField()),
                ('election_end', models.DateTimeField()),
                ('comission_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.commissioners')),
            ],
        ),
        migrations.CreateModel(
            name='Canditats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False)),
                ('election_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.election')),
            ],
        ),
        migrations.CreateModel(
            name='ElectionCategories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('election_type', models.CharField(max_length=50)),
                ('designation', models.CharField(max_length=25)),
                ('if_universe', models.BooleanField(default=False)),
                ('comission_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.commissioners')),
            ],
        ),
        migrations.AddField(
            model_name='election',
            name='election_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.electioncategories'),
        ),
        migrations.CreateModel(
            name='Observer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Identifier', models.CharField(max_length=50, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_ad', models.DateTimeField(auto_now=True)),
                ('comission_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.commissioners')),
                ('users', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Voter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Identifier', models.CharField(max_length=50, unique=True)),
                ('father_name', models.CharField(max_length=50)),
                ('mother_name', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_ad', models.DateTimeField(auto_now=True)),
                ('comission_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.commissioners')),
                ('users', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Canditate_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.canditats')),
                ('election_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.election')),
                ('voter_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.voter')),
            ],
        ),
        migrations.AddField(
            model_name='canditats',
            name='voter_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.voter'),
        ),
    ]
