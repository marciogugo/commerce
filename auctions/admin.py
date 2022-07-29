from django.contrib import admin
from .models import Comments, Listing, User

# Register your models here.

admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Comments)