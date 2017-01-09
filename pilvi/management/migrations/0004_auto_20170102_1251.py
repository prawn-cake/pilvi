# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-02 12:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0003_auto_20170102_1235'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='api',
            name='name',
        ),
        migrations.AlterField(
            model_name='proxyresource',
            name='api',
            field=models.ForeignKey(help_text='API entrypoint', on_delete=django.db.models.deletion.CASCADE, to='management.Api'),
        ),
        migrations.AlterField(
            model_name='proxyresource',
            name='endpoint_url',
            field=models.URLField(help_text='For example: http(s)://myservice:8001'),
        ),
    ]
