# Generated by Django 4.0.4 on 2022-07-21 02:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_category_listing_watchlist_comments_bid_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='listing_image_url',
        ),
    ]
