# Generated by Django 3.1.4 on 2021-01-02 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ilkapp', '0048_auto_20210103_0043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ogrencikayit',
            name='username',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
