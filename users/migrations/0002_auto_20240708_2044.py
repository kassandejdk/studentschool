# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2024-07-08 20:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='numero',
            field=models.CharField(default='', max_length=8, unique=True),
        ),
    ]
