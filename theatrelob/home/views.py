from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import json
import tmdbsimple as tmdb
# Create your views here.
from .models import Movie, Profile, WatchedItem


def index(request):
    # display a movie from tmbd api
    with open('secrets.json') as f:
        secrets = json.load(f)
        tmdb.API_KEY = secrets['tmdb_api_key']
    movies = tmdb.Movies().popular()  

    list_of_movies = []
    for movie in movies['results']:
        poster_url = 'https://image.tmdb.org/t/p/w500' + movie['poster_path']
        m = Movie(title=movie['title'], description=movie['overview'], movie_poster_url=poster_url)
        list_of_movies.append(m)

    print(list_of_movies)
    # get image url
    return render(request, 'home/index.html', {'movies': list_of_movies})
