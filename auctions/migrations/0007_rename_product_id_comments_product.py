# Generated by Django 4.0.4 on 2022-09-12 01:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_rename_product_comments_product_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comments',
            old_name='product_id',
            new_name='product',
        ),
    ]