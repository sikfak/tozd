# Generated by Django 2.0 on 2017-12-21 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_remove_cart_session_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='processed_to_order',
            field=models.BooleanField(default=False),
        ),
    ]