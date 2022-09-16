from datetime import datetime
from enum import auto
from time import timezone 
from django.contrib.auth.models import AbstractUser
from django.db import models
from .choices import CATEGORY_CHOICES, YESNO_CHOICES

class User(AbstractUser):
    def __str__(self):
        return f"First name: {self.first_name} Last name: {self.last_name} E-mail: {self.email}"

class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    listing_id = models.AutoField(primary_key=True)
    listing_category = models.CharField(max_length=150, choices=CATEGORY_CHOICES, default=None)
    listing_title = models.CharField(max_length=100)
    listing_content = models.TextField(max_length=300)
    listing_price = models.DecimalField(max_digits=8, decimal_places=2, default = 0)
    listing_image_file = models.ImageField(upload_to='media/', null=True, verbose_name="")
    listing_finished = models.CharField(max_length=1, choices=YESNO_CHOICES, default=None, null=True)

    def __str__(self):
        return f"Title: {self.listing_title} Price: {self.listing_price}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Listing, on_delete=models.CASCADE)
    def __str__(self):
        return f"Category: {self.user} Products: {self.product}"

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bid_current_value = models.DecimalField(max_digits = 8, decimal_places = 2, default = 0)
    bid_finished = models.CharField(max_length=1, choices=YESNO_CHOICES, default=None)
    def __str__(self):
        return f"Product: {Listing.listing_content} Starting Bid: {self.bid_current_value} Status: {self.bid_finished}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Listing, on_delete=models.CASCADE)
    comment_content = models.CharField(max_length=500)
    def __str__(self):
        return f"Product: {Listing.listing_title} Comment: {self.comment_content}"
