# Generated by Django 3.1.4 on 2020-12-24 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ilkapp', '0023_auto_20201224_0139'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='birebir',
            name='bbtarihi',
        ),
        migrations.AddField(
            model_name='birebir',
            name='bbgunu',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
