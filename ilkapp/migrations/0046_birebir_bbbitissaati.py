# Generated by Django 3.1.4 on 2021-01-02 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ilkapp', '0045_auto_20210102_2340'),
    ]

    operations = [
        migrations.AddField(
            model_name='birebir',
            name='bbbitissaati',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
