# Generated by Django 2.2.1 on 2019-06-03 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0014_vacancy_responded_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='vacancy',
            name='is_hiring',
            field=models.BooleanField(default=False, verbose_name='Is hiring'),
        ),
    ]
