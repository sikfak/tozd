# Generated by Django 2.0 on 2018-01-03 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_orderbillingaddress_company_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.IntegerField(choices=[(1, 'Gotovina'), (2, 'Predračun'), (3, 'Predplačilo')], default=1),
        ),
    ]
