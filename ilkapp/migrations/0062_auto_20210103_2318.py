# Generated by Django 3.1.4 on 2021-01-03 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ilkapp', '0061_auto_20210103_2302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friend',
            name='likes',
            field=models.TextField(blank=True, max_length=2000, null=True),
        ),
    ]
