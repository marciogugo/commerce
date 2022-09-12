from django.contrib import admin
from .models import Comment, Listing, User, Bid

# Register your models here.

admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Comment)
admin.site.register(Bid)