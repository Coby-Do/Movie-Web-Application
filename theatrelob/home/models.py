from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
# from django.contrib.auth.models import User
# from pinax.badges.base import Badge

class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    movie_poster_url = models.URLField(max_length=200)
    year = models.IntegerField(null=True, blank=True)
    runtime = models.IntegerField(null=True, blank=True)
    rating = models.CharField(max_length=100, null=True, blank=True)
    metascore = models.IntegerField(null=True, blank=True)
    votes = models.IntegerField(null=True, blank=True)
    gross_earning_in_mil = models.IntegerField(null=True, blank=True)
    director = models.CharField(max_length=100, null=True, blank=True)
    actor = models.CharField(max_length=100, null=True, blank=True)
    genre = models.CharField(max_length=100, null=True, blank=True)
    language = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    tmdb_id = models.IntegerField()

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()

    def __str__(self):
        return self.user.username
    
class WatchedItem(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    date_watched = models.DateField()

    def __str__(self):
        return self.movie.title

# create a model representing a third party integrationss
class Integration(models.Model):
    name = models.CharField(max_length=100)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    access_token = models.CharField(max_length=100)

    def __str__(self):
        return self.name

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# class MyBadge(Badge):
#     slug = "my-badge"

#     # Levels of difficulty for acheivement requirements
#     levels = [
#         {"name": "Bronze", "tickets": 1},
#         {"name": "Silver", "tickets": 2},
#         {"name": "Gold", "tickets": 3},
#     ]

#     # When a badge is awarded, the award method is called to update a user's profile
#     def award(self, **state):
#         user = state["user"]
#         level = state["level"]["name"]
#         message = f"{level} level {self.name} badge awarded!"
#         user.profile.badges[self.slug] = level
#         user.profile.save()
#         return message

# Defining a user's profile and storing each badge in a dictionary
# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
#     badges = models.JSONField(default=dict)
