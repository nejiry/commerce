# Generated by Django 4.0.4 on 2022-06-03 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_alter_auctions_auction_categoli_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctions',
            name='auction_price',
            field=models.IntegerField(),
        ),
    ]