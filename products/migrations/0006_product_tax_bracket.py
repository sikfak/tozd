# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-17 18:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_variation_tax_bracket'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='tax_bracket',
            field=models.DecimalField(decimal_places=2, default='22', max_digits=4),
        ),
    ]
