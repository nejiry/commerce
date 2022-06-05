# Generated by Django 4.0.4 on 2022-06-03 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_alter_auctions_auction_limittime_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctions',
            name='auction_daytime',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='auctions',
            name='auction_limittime',
            field=models.CharField(choices=[('1', '3Hours'), ('2', '12Hours'), ('3', '24Hours'), ('4', '3days')], max_length=1),
        ),
        migrations.AlterField(
            model_name='coment',
            name='coment_daytime',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='trade',
            name='trade_daitime',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]