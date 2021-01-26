# Generated by Django 3.1.4 on 2020-12-12 22:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ilkapp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, max_length=1000, null=True)),
                ('finished', models.BooleanField(default=True)),
                ('date', models.DateTimeField(blank=True, default=datetime.datetime.now, null=True)),
            ],
        ),
    ]
