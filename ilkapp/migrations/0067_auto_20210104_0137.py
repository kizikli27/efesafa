# Generated by Django 3.1.4 on 2021-01-03 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ilkapp', '0066_auto_20210104_0131'),
    ]

    operations = [
        migrations.AddField(
            model_name='dersguruplari',
            name='derssayisi',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='dersprogrami',
            name='dpgun',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
