from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Imports for recommendation system
import numpy as np
import pandas as pd
from ast import literal_eval
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity, linear_kernel


# Each genre can be assocciated with multiple movies and each movie can be associated with multiple genres
class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

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
    genres = models.ManyToManyField(Genre)
    language = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    tmdb_id = models.IntegerField()
    release_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title

# Represents the badge objects and initializes the badge data to a database
class Badge(models.Model):
    # Defines the name, description, badge_type, genre as characters
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    badge_type = models.CharField(max_length=50)
    genre = models.CharField(max_length=50, blank=True)

    # Defines the requirement as an integer
    requirement = models.IntegerField()

    # Defines a many-to-many relationship between the Badge and UserProfile models
    # (target model, allows the UserProfile to access the earned badges, allows the UserProfile to access each badge, allows badge to exist without associating with a user)
    users = models.ManyToManyField('UserProfile', related_name='earned_badges', related_query_name='badge', blank=True)

    # Returns the badge name
    def __str__(self):
        return self.name

# Properply formatting the genre's name
def format_genre_name(genre):
    if genre.lower() == "tv movie":
        return "TV Movie"
    elif genre.lower() == "science fiction":
        return "Science Fiction"
    else:
        return genre.title()

# Represents the UserProfile objects and initializes the badge data to a database
class UserProfile(models.Model):
    # Defines the user to a single user, the UserProfile's instance will be deleted if the User's instance is deleted
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Defines the number of movies watched as an integer
    movies_watched = models.PositiveIntegerField(default=0)

    # Defines the genres as integers
    action_movies_watched = models.PositiveIntegerField(default=0)
    adventure_movies_watched = models.PositiveIntegerField(default=0)
    animation_movies_watched = models.PositiveIntegerField(default=0)
    comedy_movies_watched = models.PositiveIntegerField(default=0)
    crime_movies_watched = models.PositiveIntegerField(default=0)
    documentary_movies_watched = models.PositiveIntegerField(default=0)
    drama_movies_watched = models.PositiveIntegerField(default=0)
    family_movies_watched = models.PositiveIntegerField(default=0)
    fantasy_movies_watched = models.PositiveIntegerField(default=0)
    history_movies_watched = models.PositiveIntegerField(default=0)
    horror_movies_watched = models.PositiveIntegerField(default=0)
    music_movies_watched = models.PositiveIntegerField(default=0)
    mystery_movies_watched = models.PositiveIntegerField(default=0)
    romance_movies_watched = models.PositiveIntegerField(default=0)
    science_fiction_movies_watched = models.PositiveIntegerField(default=0)
    thriller_movies_watched = models.PositiveIntegerField(default=0)
    tv_movie_movies_watched = models.PositiveIntegerField(default=0)
    war_movies_watched = models.PositiveIntegerField(default=0)
    western_movies_watched = models.PositiveIntegerField(default=0)

    # Defines the badges with the badge objects
    badges = models.ManyToManyField(Badge)

    # Returns the username
    def __str__(self):
        return self.user.username

    # Awards the user with the badge
    def award_badge(self, badge):
        self.badges.add(badge)
        self.save()

    def check_badges(self):
        # List to store the newly earned badges
        newly_earned_badges = []
        # Gets all the Badge objects from the database
        badges = Badge.objects.all()

        # Get watched movies and count genres
        genre_counts = {}

        # Iterate through watched movies associated with the user profile
        for watched_movie in self.watcheditem_set.all():
            # Checks if the movie has a genre associated with it
            if watched_movie.movie.genres.exists():
                # Creates a list of genre names for the current movie
                genres = []
                for genre in watched_movie.movie.genres.all():
                    genres.append(genre.name)

                # Updates the genre_counts dictionary 
                for genre in genres:
                    if genre in genre_counts:
                        genre_counts[genre] += 1
                    else:
                        genre_counts[genre] = 1

        # Check if the user meets the badge requirements based on the genre counts
        for badge in badges:
            # Checking for the correct badge type, validating badge requirement and whether the user already possesses the badge
            if badge.badge_type == 'movies_watched' and self.movies_watched >= badge.requirement and badge not in self.badges.all():
                self.badges.add(badge)
                newly_earned_badges.append(badge)
            elif badge.badge_type == 'genre':
                # Get the genre name associated with the badge
                genre = badge.genre
                # Format the genre name to match the defined objects from the UserProfile class
                formatted_genre = format_genre_name(genre)
                formatted_genre_name = formatted_genre.lower().replace(' ', '_')
                genre_object_name = formatted_genre_name + "_movies_watched"

                # Getting the count of watched movies for the current genre
                genre_count = getattr(self, genre_object_name, 0)
                # Validating badge requirement and whether the user already possesses the badge
                if genre_count >= badge.requirement and badge not in self.badges.all():
                    self.badges.add(badge)
                    newly_earned_badges.append(badge)

        # Return the list of newly earned badges
        return newly_earned_badges

    def update_genres_watched(self, genre):
        # Format genre name
        genre = format_genre_name(genre)

        # Mapping of genre names to UserProfile model objects
        genre_to_object = {
            "Action": "action_movies_watched",
            "Adventure": "adventure_movies_watched",
            "Animation": "animation_movies_watched",
            "Comedy": "comedy_movies_watched",
            "Crime": "crime_movies_watched",
            "Documentary": "documentary_movies_watched",
            "Drama": "drama_movies_watched",
            "Family": "family_movies_watched",
            "Fantasy": "fantasy_movies_watched",
            "History": "history_movies_watched",
            "Horror": "horror_movies_watched",
            "Music": "music_movies_watched",
            "Mystery": "mystery_movies_watched",
            "Romance": "romance_movies_watched",
            "Science Fiction": "science_fiction_movies_watched",
            "Thriller": "thriller_movies_watched",
            "TV Movie": "tv_movie_movies_watched",
            "War": "war_movies_watched",
            "Western": "western_movies_watched",
        }

        # Get the corresponding UserProfile model field for the genre
        object_name = genre_to_object.get(genre)

        if object_name:
            # Get the current value of the genre count
            current_value = getattr(self, object_name)

            # Update the genre count by adding 1
            setattr(self, object_name, current_value + 1)

            # Save the updated UserProfile model
            self.save()

    # For recommendations list
    def recommend_movies(self, movie, numofmovies=5):
        #path = "/static/csv/"  # Creates path
        credits_file = pd.read_csv("tmdb_5000_credits.csv")  # Uses panda to read file as a csv
        movies_file = pd.read_csv("tmdb_5000_movies.csv")

        recommender = MovieRecommender(credits_file, movies_file)  # Creates movie recommender object
        recommend_movies = recommender.recommend(movie)  # Calls recommender to recommend a movie
        return recommend_movies

class WatchedItem(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    date_watched = models.DateField()
    genres = models.ManyToManyField(Genre)

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
    
class MovieRecommender:
    def __init__(self, creditsfile, moviefile):
        self.creditsfile = creditsfile
        self.moviefile = moviefile

    # Function used to generate recommended movies using content based filtering
    # Takes two csvfiles and a single movie. Will take a list of movies in the future.

    def recommend(self, movieslist):

        if not (self.moviefile['title'].eq(movieslist).any()):
            return None

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
        return ' '.join(features['keywords']) + ' ' + ' '.join(features['cast']) + ' ' + features['director'] + ' ' + ' '.join(features['genres'])

    def plotrec(self, movieslist):
        if not (self.moviefile['title'].eq(movieslist).any()):
            return None

        tfidf = TfidfVectorizer(stop_words="english") # Creates a Tf-Idf vectorizer with the english stop words
        self.moviefile["overview"] = self.moviefile["overview"].fillna("")

        tfidf_matrix = tfidf.fit_transform(self.moviefile["overview"])
        cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

        indices = pd.Series(self.moviefile.index, index=self.moviefile["title"]).drop_duplicates()
        idx = indices[movieslist]
        simscore = list(enumerate(cosine_sim[idx]))
        simscore = sorted(simscore, key=lambda x: x[1], reverse=True)
        simscore = simscore[1:11]

        moviesindices = [ind[0] for ind in simscore]
        movies = self.moviefile["title"].iloc[moviesindices]
        return movies
