from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

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

class Badge(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    requirement = models.PositiveIntegerField(default=0)
    badge_type = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)  # Added bio field from Profile class
    movies_watched = models.PositiveIntegerField(default=0)
    animated_movies_watched = models.PositiveIntegerField(default=0)
    documentaries_watched = models.PositiveIntegerField(default=0)
    action_movies_watched = models.PositiveIntegerField(default=0)
    comedy_movies_watched = models.PositiveIntegerField(default=0)
    romance_movies_watched = models.PositiveIntegerField(default=0)
    badges = models.ManyToManyField(Badge)

    def __str__(self):
        return f'{self.user.username} Profile'

    def award_badge(self, badge):
        self.badges.add(badge)
        self.save()

    def check_badges(self):
        newly_earned_badges = []
        badges = Badge.objects.all()
        genres_watched = self.update_genres_watched()
        for badge in badges:
            if badge.badge_type == 'movies_watched':
                if self.movies_watched >= badge.requirement and badge not in self.badges.all():
                    self.badges.add(badge)
                    newly_earned_badges.append(badge)
            elif badge.badge_type == 'genres_watched':
                if genres_watched >= badge.requirement and badge not in self.badges.all():
                    self.badges.add(badge)
                    newly_earned_badges.append(badge)
            elif badge.badge_type == 'animated_movies_watched':
                if self.animated_movies_watched >= badge.requirement and badge not in self.badges.all():
                    self.badges.add(badge)
                    newly_earned_badges.append(badge)
            elif badge.badge_type == 'documentaries_watched':
                if self.documentaries_watched >= badge.requirement and badge not in self.badges.all():
                    self.badges.add(badge)
                    newly_earned_badges.append(badge)
            elif badge.badge_type == 'action_movies_watched':
                if self.action_movies_watched >= badge.requirement and badge not in self.badges.all():
                    self.badges.add(badge)
                    newly_earned_badges.append(badge)
            elif badge.badge_type == 'comedy_movies_watched':
                if self.comedy_movies_watched >= badge.requirement and badge not in self.badges.all():
                    self.badges.add(badge)
                    newly_earned_badges.append(badge)
            elif badge.badge_type == 'romance_movies_watched':
                if self.romance_movies_watched >= badge.requirement and badge not in self.badges.all():
                    self.badges.add(badge)
                    newly_earned_badges.append(badge)
        self.save()
        return newly_earned_badges
    
    def update_genres_watched(self):
        genre_counts = [
            self.animated_movies_watched,
            self.documentaries_watched,
            self.comedy_movies_watched,
            self.action_movies_watched,
            self.romance_movies_watched,
        ]
        genres_watched = sum(1 for count in genre_counts if count > 0)
        return genres_watched
    

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     bio = models.TextField()

#     def __str__(self):
#         return self.user.username
    
class WatchedItem(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    date_watched = models.DateField()

    def __str__(self):
        return self.movie.title

# create a model representing a third party integrationss
class Integration(models.Model):
    name = models.CharField(max_length=100)
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    access_token = models.CharField(max_length=100)

    def __str__(self):
        return self.name

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()