# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2024-07-08 20:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='course_name',
            field=models.CharField(max_length=20),
        ),
    ]
