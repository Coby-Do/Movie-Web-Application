from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import json
import tmdbsimple as tmdb
# Create your views here.

def index(request):
    # display a movie from tmbd api
    with open('secrets.json') as f:
        secrets = json.load(f)
        tmdb.API_KEY = secrets['tmdb_api_key']
    movie = tmdb.Movies(550)
    movie.info()
    # get image url
    poster_url = 'https://image.tmdb.org/t/p/w500' + movie.poster_path
    return render(request, 'home/index.html', {'movie_title': movie.title, 'movie_overview': movie.overview, 
    'movie_poster': poster_url, 'movie_backdrop': movie.backdrop_path})
