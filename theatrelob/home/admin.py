from django.contrib import admin

# Register your models here.
from .models import Movie, Profile, WatchedItem

admin.site.register(Movie)
admin.site.register(Profile)
admin.site.register(WatchedItem)
