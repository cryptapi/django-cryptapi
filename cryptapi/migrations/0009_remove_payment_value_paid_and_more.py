# Generated by Django 4.1.4 on 2023-01-19 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cryptapi', '0008_metadata_alter_provider_coin_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='value_paid',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='value_received',
        ),
        migrations.AddField(
            model_name='payment',
            name='value_fee_coin',
            field=models.DecimalField(decimal_places=18, default=0, help_text='CryptAPI Fee.', max_digits=65, verbose_name='Fee Coin'),
        ),
        migrations.AddField(
            model_name='payment',
            name='value_price',
            field=models.DecimalField(decimal_places=18, default=0, help_text='Coin price in USD at the time of receiving.', max_digits=65, verbose_name='Price Coin in USD'),
        ),
        migrations.AlterField(
            model_name='metadata',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='payment',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='paymentlog',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='provider',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='request',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='requestlog',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
