# Generated by Django 4.0.4 on 2022-08-23 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auction'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]