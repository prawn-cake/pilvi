# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-04 14:07
from __future__ import unicode_literals

from django.db import migrations

from pilvi.management.helpers import create_http_methods


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('management', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_http_methods)
    ]
