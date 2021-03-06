# Generated by Django 2.2.1 on 2019-05-13 13:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0011_auto_20190513_1317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follow',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follows', to='companies.Company', verbose_name='Company'),
        ),
        migrations.AlterField(
            model_name='follow',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follows', to=settings.AUTH_USER_MODEL, verbose_name='Owner'),
        ),
    ]
