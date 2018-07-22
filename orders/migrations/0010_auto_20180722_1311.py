# Generated by Django 2.0 on 2018-07-22 11:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20171225_2225'),
        ('orders', '0009_order_payment_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='distributer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.Distributer'),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.IntegerField(choices=[(1, 'Gotovina'), (2, 'Predračun'), (3, 'Predplačilo')], default=2),
        ),
    ]