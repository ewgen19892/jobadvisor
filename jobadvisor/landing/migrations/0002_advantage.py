# Generated by Django 2.2.2 on 2019-06-05 08:53

from django.db import migrations, models
import jobadvisor.common.helpers


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Advantage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Name')),
                ('file', models.ImageField(upload_to=jobadvisor.common.helpers.upload_to, verbose_name='File')),
                ('weight', models.SmallIntegerField(default=1, verbose_name='Weight')),
            ],
            options={
                'verbose_name': 'Advantage',
                'verbose_name_plural': 'Advantages',
                'ordering': ['weight'],
            },
        ),
    ]
