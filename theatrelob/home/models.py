from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Imports for recommendation system
import numpy as np
import tmdbsimple as tmdb
import pandas as pd
from ast import literal_eval
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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

    # For recommendations list
    def recommend_movies(self, movie, numofmovies=5):
        #path = "/static/csv/"  # Creates path
        credits_file = pd.read_csv("static/csv/tmdb_5000_credits.csv")  # Uses panda to read file as a csv
        movies_file = pd.read_csv("static/csv/tmdb_5000_movies.csv")

        recommender = MovieRecommender(credits_file, movies_file)  # Creates movie recommender object
        recommend_movies = recommender.recommend(movie)  # Calls recommender to recommend a movie
        return recommend_movies
    
class MovieRecommender:
    def __init__(self, creditsfile, moviefile):
        self.creditsfile = creditsfile
        self.moviefile = moviefile

    # Function used to generate recommended movies using content based filtering
    # Takes two csvfiles and a single movie. Will take a list of movies in the future.

    def recommend(self, movieslist):
        self.creditsfile.columns = ['id', 'title', 'cast', 'crew']  # takes only id, title, cast, and crew columns

        self.moviefile = self.moviefile.merge(self.creditsfile, on="title")  # merges the dataframes using the id
        features = ["cast", "crew", "keywords", "genres"]  # build recommendation off these features

        for feature in features:  # converts data into usable structure. data is lists of strings until we convert
            self.moviefile[feature] = self.moviefile[feature].apply(literal_eval)

        self.moviefile["director"] = self.moviefile["crew"].apply(self.getdirector)  # gets directors
        features = ["cast", "keywords", "genres"]
        for feature in features:
            self.moviefile[feature] = self.moviefile[feature].apply(self.getlist)  # takes top 3 keywords of the features

        features = ['cast', 'keywords', 'director', 'genres']
        for feature in features:
            self.moviefile[feature] = self.moviefile[feature].apply(self.cleandata)  # removes spaces and lowercases everything
        self.moviefile["phrases"] = self.moviefile.apply(self.prepvectorizer, axis=1)

        countvectorizer = CountVectorizer(stop_words="english")
        countmatrix = countvectorizer.fit_transform(self.moviefile["phrases"])

        cosine_sim2 = cosine_similarity(countmatrix, countmatrix)

        self.moviefile = self.moviefile.reset_index()
        indices = pd.Series(self.moviefile.index, index=self.moviefile['title'])

        idx = indices[movieslist]
        simscore = list(enumerate(cosine_sim2[idx]))
        simscore = sorted(simscore, key=lambda x: x[1], reverse=True)
        simscore = simscore[1:11]

        moviesindices = [ind[0] for ind in simscore]
        movies = self.moviefile["title"].iloc[moviesindices]
        return movies

    # Loops over the crew for a movie to see if anyone is a director.
    # Takes a crew and returns a person who is a director or none.
    def getdirector(self, crew):
        for person in crew:
            if person["job"] == "Director":
                return person["name"]
            return np.nan

    # Takes the top 3 elements of the list or the entire list if there are less than 3 elements.
    # Takes a list and returns the top 3 elements of the entire list.
    def getlist(self, x):
        if isinstance(x, list):
            names = [i["name"] for i in x]

            if len(names) > 3:
                names = names[:3]

            return names
        return []

    # Function that cleans the instances by converting to lowercase and removing the spaces. Takes an instance of the data
    def cleandata(self, row):
        if isinstance(row, list):
            return [str.lower(i.replace(" ", "")) for i in row]
        else:
            if isinstance(row, str):
                return str.lower(row.replace(" ", ""))
            else:
                return ""

    # Function that prepares the data to be input into the vectorizer. Takes feature as input
    def prepvectorizer(self, features):
        return ' '.join(features['keywords']) + ' ' + ' '.join(features['cast']) + ' ' + features[
            'director'] + ' ' + ' '.join(features['genres'])


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