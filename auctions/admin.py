from django.contrib import admin
from .models import Category, Comments, Listing, User

# Register your models here.

admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Category)
admin.site.register(Comments)