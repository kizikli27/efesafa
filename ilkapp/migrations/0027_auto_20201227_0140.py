# Generated by Django 3.1.4 on 2020-12-26 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ilkapp', '0026_hafta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='birebir',
            name='bbgunu',
            field=models.PositiveIntegerField(blank=True, max_length=1, null=True),
        ),
    ]
