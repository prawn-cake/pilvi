# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-04 14:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import pilvi.management.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApiEndpoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(help_text='For example: /api/v1 .This endpoint will be available as http(s)://0.0.0.0/api/v1', max_length=2083, unique=True, validators=[pilvi.management.models.validate_endpoint])),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True)),
                ('api_key', models.CharField(max_length=256, unique=True)),
                ('is_active', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='HTTPMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('GET', 'GET'), ('POST', 'POST'), ('PUT', 'PUT'), ('DELETE', 'DELETE'), ('PATCH', 'PATCH'), ('HEAD', 'HEAD')], max_length=10, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProxyResource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('url', models.URLField()),
                ('endpoint', models.ForeignKey(help_text='API endpoint', on_delete=django.db.models.deletion.CASCADE, to='management.ApiEndpoint')),
                ('methods', models.ManyToManyField(to='management.HTTPMethod')),
            ],
        ),
    ]