from django.contrib import admin

# Register your models here.
from .models import Movie, UserProfile, WatchedItem, Badge, Genre, Integration, MovieRecommender 

admin.site.register(Movie)
admin.site.register(UserProfile)
admin.site.register(WatchedItem)
admin.site.register(Badge)
admin.site.register(Genre)
admin.site.register(Integration)
