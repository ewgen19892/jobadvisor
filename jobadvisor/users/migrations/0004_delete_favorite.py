# Generated by Django 2.2.1 on 2019-05-13 12:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20190511_0954'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Favorite',
        ),
    ]