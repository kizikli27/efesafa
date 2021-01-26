# Generated by Django 3.1.4 on 2021-01-09 20:50

from django.db import migrations
import django_thumbs.fields


class Migration(migrations.Migration):

    dependencies = [
        ('ilkapp', '0069_auto_20210107_0120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kurums',
            name='logo',
            field=django_thumbs.fields.ImageThumbsField(sizes=({'code': 'avatar', 'resize': 'crop', 'wxh': '125x125'}, {'code': 'm', 'resize': 'scale', 'wxh': '640x480'}, {'code': '150', 'wxh': '150x150'}), upload_to='logom'),
        ),
    ]
