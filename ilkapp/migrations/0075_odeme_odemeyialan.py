# Generated by Django 3.1.4 on 2021-01-12 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ilkapp', '0074_ogretmenkayit_muhasebe'),
    ]

    operations = [
        migrations.AddField(
            model_name='odeme',
            name='odemeyialan',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
