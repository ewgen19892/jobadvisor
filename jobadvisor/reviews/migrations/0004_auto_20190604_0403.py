# Generated by Django 2.2.1 on 2019-06-04 04:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_auto_20190529_1149'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='finished_at',
        ),
        migrations.RemoveField(
            model_name='review',
            name='started_at',
        ),
    ]