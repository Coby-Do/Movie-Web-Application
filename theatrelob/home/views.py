from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
import json
import tmdbsimple as tmdb
from .models import Movie, Profile, WatchedItem
from django.contrib.auth.decorators import login_required
from pinax.badges.models import BadgeAward
from .models import MyBadge
from django.contrib import messages
from django.contrib.auth.models import User
# from.models import UserProfile

def index(request):
    # display a movie from tmbd api
    with open('secrets.json') as f:
        secrets = json.load(f)
        tmdb.API_KEY = secrets['tmdb_api_key']
    movies = tmdb.Movies().popular()  
    batch_of_three_movies = []
    list_of_movies = []
    for movie in movies['results']:
        poster_url = 'https://image.tmdb.org/t/p/w500' + movie['poster_path']
        m = Movie(title=movie['title'], description=movie['overview'], movie_poster_url=poster_url)
       
        batch_of_three_movies.append(m)
        if len(batch_of_three_movies) == 3:
            list_of_movies.append(batch_of_three_movies)
            batch_of_three_movies = []

    print(list_of_movies)
    # get image url
    return render(request, 'home/index.html', {'movies': list_of_movies})

@login_required(login_url='accounts/login/')
def watchlist(request):
    # retrieve all watched items from the database belonging to the user
    # display them on the page
    # get the user's id
    user_id = request.user.id

    # get the user's profile
    profile = Profile.objects.get(user_id=user_id)
    # get the user's watched items
    watched_items = WatchedItem.objects.filter(user=profile.user)
    
    # display the watched items
    return render(request, 'home/watchlist.html', {'watched_items': watched_items})
    
def add_to_watchlist(request):
    # get the user's id
    user_id = request.user.id

    # get the user's profile
    profile = Profile.objects.get(user_id=user_id)
    # get the movie's id
    movie_id = request.POST['movie_id']
    #if it doesn't exist, create it
    if not Movie.objects.filter(id=movie_id).exists():
        with open('secrets.json') as f:
            secrets = json.load(f)
            tmdb.API_KEY = secrets['tmdb_api_key']
        movie = tmdb.Movies(movie_id).info()
        poster_url = 'https://image.tmdb.org/t/p/w500' + movie['poster_path']
        m = Movie(id=movie_id, title=movie['title'], description=movie['overview'], movie_poster_url=poster_url)
        m.save()
    # get the movie
    movie = Movie.objects.get(id=movie_id)
    # add the movie to the user's watchlist
    watched_item = WatchedItem(user=profile.user, movie=movie)
    watched_item.save()
    # redirect to the watchlist page
    return redirect('watchlist')

@login_required
# Renders a view when a badge is rewarded to a user
def award_my_badge(request):
    badge = MyBadge(request.user)
    award = badge.get_next_level()
    message = badge.award(user=request.user, level=award)
    BadgeAward.objects.create(badge=badge, user=request.user, level=award)

    return render(request, "badges/award_my_badge.html", {"message": message})


# @login_required
# Renders a view when the user earns tickets
# def award_tickets(request):
#     if request.method == 'POST':
#         user = request.user
#         num_tickets = request.POST.get('num_tickets')

#         # Update the user's profile with the awarded tickets
#         profile = UserProfile.objects.get(user=user)
#         profile.tickets += int(num_tickets)
#         profile.save()

#         # Display a success message
#         messages.success(request, f"{num_tickets} tickets awarded to {user.username}")

#         return redirect('award_tickets')

#     return render(request, 'badges/award_tickets.html')
