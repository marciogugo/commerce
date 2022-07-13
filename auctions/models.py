from unicodedata import category
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    def __str__(self):
        return f"First name: {self.first_name} Last name: {self.last_name} E-mail: {self.email}"

class Listing(models.Model):
    LISTING_STATUS = [
        ('A', 'Available'),
        ('U', 'Unavailable'),
        ('S', 'Sold out')
    ]
    listing_title = models.CharField(max_length=100)
    listing_content = models.TextField
    listing_price = models.DecimalField
    listing_stock = models.IntegerField
    listing_status = models.CharField(max_length=1, choices = LISTING_STATUS)
    listing_image_url = models.URLField
    listing_start_date = models.DateField
    listing_end_date = models.DateField
    def __str__(self):
        return f"Title: {self.listing_title} Price: {self.listing_price} Status: {self.listing_status}"

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=20)
    def __str__(self):
        return f"Name: {self.category_name}"

class CategoryListing(Category, Listing):
    categories = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="categories_listings")
    products = models.ManyToManyField('Listing', related_name='categories_listings')
    def __str__(self):
        return f"Category: {self.categories} Products: {self.products}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Listing, on_delete=models.CASCADE)

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bid_starting_value = models.DecimalField
    bid_current_value = models.DecimalField
    bid_start_date_time = models.DateTimeField
    bid_finish_date_time = models.DateTimeField
    def __str__(self):
        return f"Product: {models.product.listing.content} Starting Bid: {self.bid_starting_value} Status: {self.bid_current_value}"

class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Listing, on_delete=models.CASCADE)
    comment_content = models.CharField(max_length=500)
    def __str__(self):
        return f"Product: {models.product.listing.title} Comment: {self.comment_content}"
