# Generated by Django 3.1.4 on 2020-12-26 23:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ilkapp', '0031_birebir_bbgun'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='birebir',
            name='bbgun',
        ),
        migrations.RemoveField(
            model_name='birebir',
            name='bbgunu',
        ),
    ]
