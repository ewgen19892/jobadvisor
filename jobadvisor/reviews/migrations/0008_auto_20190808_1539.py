# Generated by Django 2.2.3 on 2019-08-08 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0007_review_is_hiring'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='is_hiring',
        ),
        migrations.AddField(
            model_name='review',
            name='is_best',
            field=models.BooleanField(default=False, verbose_name='This is the best'),
        ),
    ]
