# Generated by Django 2.2.1 on 2019-05-15 07:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
        ('companies', '0013_auto_20190513_1325'),
    ]

    operations = [
        migrations.CreateModel(
            name='Interview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120, verbose_name='Title')),
                ('description', models.TextField(verbose_name='Description')),
                ('experience', models.PositiveSmallIntegerField(choices=[(2, 'Positive'), (1, 'No opinion'), (0, 'Negative')], default=1, verbose_name='Experience')),
                ('complication', models.PositiveSmallIntegerField(verbose_name='Complication')),
                ('has_offer', models.BooleanField(null=True, verbose_name='Has offer')),
                ('duration', models.PositiveSmallIntegerField(help_text='In minutes', null=True, verbose_name='duration')),
                ('date', models.DateField(null=True, verbose_name='Date')),
                ('place', models.CharField(max_length=120, null=True, verbose_name='Place')),
                ('is_anonymous', models.BooleanField(default=True, verbose_name='Is anonymous')),
                ('is_top', models.BooleanField(default=False, verbose_name='Is TOP')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interviews', to='companies.Company', verbose_name='Company')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interviews', to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interviews', to='companies.Position', verbose_name='Position')),
            ],
            options={
                'verbose_name': 'Interview',
                'verbose_name_plural': 'Interviews',
                'ordering': ['-pk'],
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120, verbose_name='Title')),
                ('description', models.TextField(verbose_name='Description')),
                ('rate', models.PositiveSmallIntegerField()),
                ('improvements', models.TextField(null=True, verbose_name='Improvements')),
                ('started_at', models.DateField(verbose_name='Started working at')),
                ('finished_at', models.DateField(null=True, verbose_name='Finished working at')),
                ('is_anonymous', models.BooleanField(default=True, verbose_name='Is anonymous')),
                ('is_top', models.BooleanField(default=False, verbose_name='Is TOP')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='companies.Company', verbose_name='Company')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
            ],
            options={
                'verbose_name': 'Review',
                'verbose_name_plural': 'Reviews',
                'ordering': ['-pk'],
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Text')),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Open'), (1, 'In progress'), (2, 'Closed')], default=0, verbose_name='Status')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
            ],
            options={
                'verbose_name': 'Report',
                'verbose_name_plural': 'Reports',
                'ordering': ['-pk'],
            },
        ),
        migrations.CreateModel(
            name='QA',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField(verbose_name='Question')),
                ('answer', models.TextField(verbose_name='Answer')),
                ('interview', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='qas', to='reviews.Interview', verbose_name='Interview')),
            ],
            options={
                'verbose_name': 'Question & answer',
                'verbose_name_plural': 'Questions & answers',
                'ordering': ['-pk'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Text')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
                'ordering': ['-pk'],
            },
        ),
    ]
