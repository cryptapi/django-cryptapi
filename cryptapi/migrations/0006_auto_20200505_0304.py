# Generated by Django 3.0.2 on 2020-05-05 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cryptapi', '0005_auto_20200504_2323'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='value_paid_coin',
            field=models.DecimalField(decimal_places=18, default=0, max_digits=65, verbose_name='Value Paid Coin'),
        ),
        migrations.AddField(
            model_name='payment',
            name='value_received_coin',
            field=models.DecimalField(decimal_places=18, default=0, max_digits=65, verbose_name='Value Received Coin'),
        ),
    ]