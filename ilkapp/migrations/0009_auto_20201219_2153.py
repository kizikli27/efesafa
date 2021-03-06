# Generated by Django 3.1.4 on 2020-12-19 18:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ilkapp', '0008_delete_ogrenci'),
    ]

    operations = [
        migrations.AddField(
            model_name='ogrencikayit',
            name='alani',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='ogrencikayit',
            name='birebirsaati',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='ogrencikayit',
            name='kayittarihi',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now, null=True),
        ),
        migrations.AddField(
            model_name='ogrencikayit',
            name='okulu',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='ogrencikayit',
            name='veliadi',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='ogrencikayit',
            name='velitelefonu',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='ogrencikayit',
            name='telefonu',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='ogrencikayit',
            name='username',
            field=models.CharField(blank=True, max_length=11, null=True),
        ),
    ]
