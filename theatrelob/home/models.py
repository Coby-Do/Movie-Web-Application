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

    def __str__(self):
        return self.title


<<<<<<< Updated upstream
class Profile(models.Model):
=======
    def __str__(self):
        return self.name

class UserProfile(models.Model):
>>>>>>> Stashed changes
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()

    def __str__(self):
<<<<<<< Updated upstream
        return self.user.username
=======
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
>>>>>>> Stashed changes
    
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

