# Generated by Django 3.1.4 on 2020-12-20 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ilkapp', '0015_auto_20201220_1730'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ogrencikayit',
            name='kurum',
        ),
        migrations.RemoveField(
            model_name='ogretmenkayit',
            name='kurum',
        ),
        migrations.AddField(
            model_name='ogrencikayit',
            name='nim',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name='ogretmenkayit',
            name='nim',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
