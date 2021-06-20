# Generated by Django 2.2.4 on 2019-08-12 09:09

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0007_page'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='page',
            options={'ordering': ('pk',)},
        ),
        migrations.AlterField(
            model_name='page',
            name='slug',
            field=models.SlugField(help_text='Do not change this field', unique=True, verbose_name='Page slug'),
        ),
        migrations.AlterField(
            model_name='page',
            name='text',
            field=ckeditor.fields.RichTextField(verbose_name='Page text'),
        ),
    ]