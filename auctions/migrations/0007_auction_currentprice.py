# Generated by Django 4.0.4 on 2022-08-23 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auction_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='currentPrice',
            field=models.IntegerField(default=0, help_text='Not to exceed 2147483647!'),
            preserve_default=False,
        ),
    ]
