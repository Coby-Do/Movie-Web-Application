from django.contrib import admin

# Register your models here.
from .models import Movie, UserProfile, WatchedItem

admin.site.register(Movie)
admin.site.register(UserProfile)
admin.site.register(WatchedItem)
