# Generated by Django 2.2.1 on 2019-05-03 16:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0002_auto_20190502_1501'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='plan',
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan', models.PositiveIntegerField(choices=[(1, 'First'), (2, 'Second'), (3, 'Third')], verbose_name='Plan')),
                ('started_at', models.DateTimeField(auto_now_add=True, verbose_name='Started at')),
                ('finished_at', models.DateTimeField(verbose_name='Finished at')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to='companies.Company', verbose_name='Company')),
            ],
            options={
                'verbose_name': 'Subscription',
                'verbose_name_plural': 'Subscriptions',
                'ordering': ['pk'],
            },
        ),
    ]
