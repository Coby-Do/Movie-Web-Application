from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
from django.contrib.auth.models import User
from pinax.badges.base import Badge

class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    movie_poster_url = models.URLField(max_length=200)
    year = models.IntegerField()
    runtime = models.IntegerField()
    rating = models.CharField(max_length=100)
    metascore = models.IntegerField()
    votes = models.IntegerField()
    gross_earning_in_mil = models.IntegerField()
    director = models.CharField(max_length=100)
    actor = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    language = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    tmdb_id = models.IntegerField()

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()

    def __str__(self):
        return self.user.username
    
class WatchedItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    date_watched = models.DateField()

    def __str__(self):
        return self.movie.title


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class MyBadge(Badge):
    slug = "my-badge"

    # Levels of difficulty for acheivement requirements
    levels = [
        {"name": "Bronze", "tickets": 1},
        {"name": "Silver", "tickets": 2},
        {"name": "Gold", "tickets": 3},
    ]

    # When a badge is awarded, the award method is called to update a user's profile
    def award(self, **state):
        user = state["user"]
        level = state["level"]["name"]
        message = f"{level} level {self.name} badge awarded!"
        user.profile.badges[self.slug] = level
        user.profile.save()
        return message

# Defining a user's profile and storing each badge in a dictionary
# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
#     badges = models.JSONField(default=dict)
