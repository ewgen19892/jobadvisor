# Generated by Django 2.2.1 on 2019-05-13 13:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0010_auto_20190513_1313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='followers',
            field=models.ManyToManyField(through='companies.Follow', to=settings.AUTH_USER_MODEL, verbose_name='followers'),
        ),
        migrations.AlterField(
            model_name='follow',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to=settings.AUTH_USER_MODEL, verbose_name='Owner'),
        ),
    ]
