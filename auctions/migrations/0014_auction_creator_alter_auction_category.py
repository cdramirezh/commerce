# Generated by Django 4.0.4 on 2022-08-25 16:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_bid'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='creator',
            field=models.ForeignKey(default=6, on_delete=django.db.models.deletion.CASCADE, related_name='created_auctions', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='auction',
            name='category',
            field=models.CharField(blank=True, choices=[('FA', 'Fashion'), ('TO', 'Toys'), ('EL', 'Electronics'), ('HO', 'Home')], max_length=2),
        ),
    ]
