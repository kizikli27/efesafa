# Generated by Django 3.1.4 on 2020-12-29 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ilkapp', '0034_auto_20201229_0128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mesajlar',
            name='resim',
            field=models.FileField(blank=True, upload_to='mesajimg'),
        ),
    ]
