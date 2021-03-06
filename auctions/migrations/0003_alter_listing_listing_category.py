# Generated by Django 4.0.4 on 2022-07-29 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_listing_watchlist_comments_bid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='listing_category',
            field=models.CharField(choices=[('Electronics', (('Computers & Tablets', 'Computers & Tablets'), ('Cameras & Photo', 'Cameras & Photo'), ('Home Surveillance Systems', 'Home Surveillance Systems'), ('Gaming', 'Gaming'), ('Cell Phones, Smart Watches & Accessories', 'Cell Phones, Smart Watches & Accessories'), ('TV, Video & Home Audio Electronics', 'TV, Video & Home Audio Electronics'))), ('Fashion', (('Men', 'Men'), ('Women', 'Women'), ('Kids', 'Kids'))), ('Sports', (('Cycling', 'Cycling'), ('Fitness, Running & Yoga', 'Fitness, Running & Yoga'), ('Outdoor Sports', 'Outdoor Sports'), ('Tactical & Duty Gear', 'Tactical & Duty Gear'), ('Water Sports', 'Water Sports')))], default=None, max_length=150),
        ),
    ]
