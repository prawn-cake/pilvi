# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-02 12:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0002_auto_20161213_0649'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='resources',
            field=models.ManyToManyField(to='management.ProxyResource'),
        ),
        migrations.AlterField(
            model_name='client',
            name='api_key',
            field=models.CharField(editable=False, max_length=256, unique=True),
        ),
        migrations.AlterField(
            model_name='proxyresource',
            name='protected',
            field=models.BooleanField(default=True, help_text='Indicates that resource is protected with token'),
        ),
    ]
