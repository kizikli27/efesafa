# Generated by Django 3.1.4 on 2021-01-02 23:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ilkapp', '0054_auto_20210103_0223'),
    ]

    operations = [
        migrations.AddField(
            model_name='duyurular',
            name='dtarih',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now, null=True),
        ),
    ]
