# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-16 22:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0002_zabojproduction_assign_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zabojproduction',
            name='distribution_notes',
            field=models.TextField(blank=True, max_length=140, null=True),
        ),
        migrations.AlterField(
            model_name='zabojproduction',
            name='enduser_notes',
            field=models.TextField(blank=True, max_length=140, null=True),
        ),
    ]
