# Generated by Django 2.2 on 2019-05-02 15:01

from django.db import migrations, models
import django.db.models.deletion
import jobadvisor.common.helpers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, unique=True, verbose_name='Name')),
                ('logo', models.ImageField(null=True, upload_to=jobadvisor.common.helpers.upload_to, verbose_name='Logotype')),
                ('website', models.URLField(null=True, verbose_name='Website')),
                ('size', models.PositiveIntegerField(null=True, verbose_name='Size')),
                ('founded', models.DateField(null=True, verbose_name='Founded date')),
                ('description', models.TextField(null=True, verbose_name='Description')),
                ('plan', models.CharField(choices=[('first', 'First plan'), ('second', 'Second plan'), ('third', 'Third plan')], default='first', max_length=12, verbose_name='Plan')),
                ('is_validated', models.BooleanField(default=False, verbose_name='Is validated')),
                ('is_banned', models.BooleanField(default=False, verbose_name='Is banned')),
                ('deleted_at', models.DateTimeField(null=True, verbose_name='Deleted at')),
            ],
            options={
                'verbose_name': 'Company',
                'verbose_name_plural': 'Companies',
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='Industry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Industry',
                'verbose_name_plural': 'Industry',
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Position',
                'verbose_name_plural': 'Positions',
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(verbose_name='Description')),
                ('salary', models.PositiveIntegerField(verbose_name='Salary')),
                ('experience', models.FloatField(verbose_name='Experience in years')),
                ('location', models.CharField(max_length=255, verbose_name='Location')),
                ('level', models.SmallIntegerField(choices=[(0, 'Trainee'), (1, 'Employee')], default=1, verbose_name='Candidate level')),
                ('deleted_at', models.DateTimeField(null=True, verbose_name='Deleted at')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vacancies', to='companies.Company', verbose_name='Company')),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vacancies', to='companies.Position', verbose_name='Position')),
            ],
            options={
                'verbose_name': 'Vacancy',
                'verbose_name_plural': 'Vacancies',
                'ordering': ['pk'],
            },
        ),
    ]
