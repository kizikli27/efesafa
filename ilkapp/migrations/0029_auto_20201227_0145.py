# Generated by Django 3.1.4 on 2020-12-26 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ilkapp', '0028_auto_20201227_0141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='birebir',
            name='bbgunu',
            field=models.PositiveSmallIntegerField(blank=True, max_length=2, null=True),
        ),
    ]
