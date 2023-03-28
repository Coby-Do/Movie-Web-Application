from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import json
import tmdbsimple as tmdb
from django.shortcuts import redirect
from .models import Movie, Profile, WatchedItem
from django.contrib.auth.decorators import login_required
<<<<<<< Updated upstream
=======
# For recommend
import pandas as pd
import os
from django.conf import settings

from django.shortcuts import render, get_object_or_404
from .models import UserProfile, MovieRecommender
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Badge
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
>>>>>>> Stashed changes



def index(request):
    # display a movie from tmbd api
    with open('secrets.json') as f:
        secrets = json.load(f)
        tmdb.API_KEY = secrets['tmdb_api_key']
<<<<<<< Updated upstream
    movies = tmdb.Movies().popular()  

=======
    movies = tmdb.Movies().popular()
    batch_of_three_movies = []
>>>>>>> Stashed changes
    list_of_movies = []
    for movie in movies['results']:
        poster_url = 'https://image.tmdb.org/t/p/w500' + movie['poster_path']
        m = Movie(title=movie['title'], description=movie['overview'], movie_poster_url=poster_url)
        list_of_movies.append(m)

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
<<<<<<< Updated upstream
    watched_items = WatchedItem.objects.filter(user=profile.user)
    
=======
    watched_items = WatchedItem.objects.filter(profile=profile)

>>>>>>> Stashed changes
    # display the watched items
    return render(request, 'home/watchlist.html', {'watched_items': watched_items})
    
def add_to_watchlist(request):
    # get the user's id
    user_id = request.user.id

    # get the user's profile
<<<<<<< Updated upstream
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
=======
    profile = UserProfile.objects.get(user_id=user_id)

    # get the movie's id from the POST parameter
    movie_id = request.POST.get('movie_id', None)

    if movie_id is not None:
        # check if the movie exists in the database
        if not Movie.objects.filter(id=movie_id).exists():
             with open('secrets.json') as f:
                 secrets = json.load(f)
                 tmdb.API_KEY = secrets['tmdb_api_key']
            movie = tmdb.Movies(movie_id).info()
            poster_url = 'https://image.tmdb.org/t/p/w500' + movie['poster_path']
            m = Movie(id=movie_id, title=movie['title'], description=movie['overview'], movie_poster_url=poster_url, tmdb_id=movie_id)
            m.save()

        # get the movie
        movie = Movie.objects.get(id=movie_id)

        # add the movie to the user's watchlist
        date = datetime.date.today()

        watched_item = WatchedItem(profile=profile, movie=movie, date_watched=date)
        watched_item.save()

        # redirect to the watchlist page
        return redirect('watchlist')

@login_required(login_url='accounts/login/')
def get_access_token(request):
    # get the user's id
    user_id = request.user.id
    access_token = request.POST['code']

    # create an integration for the user
    # get the profile
    profile = UserProfile.objects.get(user_id=user_id)
    integration = Integration(profile=profile, name="Test", access_token=access_token)
    integration.save()


    # return a json with the access token
    return HttpResponse(json.dumps({'access_token': access_token}), content_type='application/json')

def randomrec(request):
     with open('secrets.json') as f:
         secrets = json.load(f)
         tmdb.API_KEY = secrets['tmdb_api_key']
    latestMovie = tmdb.Movies().latest()
    movieId     = latestMovie['id']

    randomNum   = random.randint(1, movieId)
    randomMovie = tmdb.Movies(randomNum)

    response         = randomMovie.info()
    randomMovieTitle = randomMovie.title

    context = {'randomMovieTitle': randomMovieTitle}

    return render(request, 'home/randomrec.html', context)

# Profile views

@login_required

def home(request):
    return render(request, 'profiles/home.html')

class CustomLoginView(LoginView):
    template_name = 'home/login.html'

def logout_view(request):
    logout(request)
    return redirect('index')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Check if a UserProfile already exists for the user
            if not UserProfile.objects.filter(user=user).exists():
                UserProfile.objects.create(user=user)  # Create a UserProfile for the new user
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'profile/register.html', {'form': form})


def profile(request, username):
    if request.user.is_authenticated and request.user.username == username:
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.check_badges()
        user_profile.refresh_from_db()  # Refresh the user_profile instance from the database
        # return render(request, 'profiles/profile.html', {'profile': user_profile})
        return render(request, 'profile/profile.html', {'profile': user_profile})
    else:
        return HttpResponseRedirect(reverse('index'))

def badge_list(request):
    if request.user.is_authenticated:
        badges = Badge.objects.all()
        profile = UserProfile.objects.get(user=request.user)
        return render(request, 'profile/badge_list.html', {'badges': badges, 'profile': profile})
    else:
        return HttpResponseRedirect(reverse('index'))

def create_badges(request):
    badges_data = [
        {
            'name': '10 Movies Watched',
            'description': 'Watched 10 movies.',
            'type': 'movies_watched',
            'requirement': 10
        },
        {
            'name': '20 Movies Watched',
            'description': 'Watched 20 movies.',
            'type': 'movies_watched',
            'requirement': 20
        },
        {
            'name': 'Genre Enthusiast',
            'description': 'Watched movies from 5 different genres.',
            'type': 'genres_watched',
            'requirement': 5
        },
        {
            'name': 'Animation Fan',
            'description': 'Watched 5 animated movies.',
            'type': 'animated_movies_watched',
            'requirement': 5
        },
        {
            'name': 'Documentary Buff',
            'description': 'Watched 3 documentaries.',
            'type': 'documentaries_watched',
            'requirement': 3
        },
        {
            'name': 'Action Lover',
            'description': 'Watched 5 action movies.',
            'type': 'action_movies_watched',
            'requirement': 5
        },
        {
            'name': 'Comedy Fan',
            'description': 'Watched 5 comedy movies.',
            'type': 'comedy_movies_watched',
            'requirement': 5
        },
        {
            'name': 'Romance Enthusiast',
            'description': 'Watched 5 romance movies.',
            'type': 'romance_movies_watched',
            'requirement': 5
        },

        # Add more badges here as needed
    ]

    for badge_data in badges_data:
        Badge.objects.get_or_create(
            name=badge_data['name'],
            description=badge_data['description'],
            badge_type=badge_data.get('type'),
            requirement=badge_data.get('requirement', 0),
        )

    return HttpResponse("Badges created!")

def watch_movie(request):
    user_profile = UserProfile.objects.get(user=request.user)
    user_profile.movies_watched += 1
    user_profile.save()
    newly_earned_badges = user_profile.check_badges()

    for badge in newly_earned_badges:
        messages.success(request, f'Congratulations! You earned the "{badge.name}" badge!')

    username = request.user.username
    return redirect('profile', username=username)

def reset_user_badges(request):
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.badges.clear()
        user_profile.movies_watched = 0
        user_profile.animated_movies_watched = 0
        user_profile.documentaries_watched = 0
        user_profile.action_movies_watched = 0
        user_profile.comedy_movies_watched = 0
        user_profile.romance_movies_watched = 0
        user_profile.save()
        print("User badges cleared for user:", request.user.username)
        return HttpResponseRedirect(reverse('profile', args=[request.user.username]))
    else:
        return HttpResponseRedirect(reverse('index'))

def delete_badges(request):
    Badge.objects.all().delete()
    return HttpResponse("Badges deleted!")

def watch_animation(request):
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.animated_movies_watched += 1
        user_profile.movies_watched += 1
        user_profile.save()
        user_profile.check_badges()
        user_profile.refresh_from_db()
        return redirect('profile', request.user.username)
    else:
        return HttpResponseRedirect(reverse('index'))

def watch_documentary(request):
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.documentaries_watched += 1
        user_profile.movies_watched += 1
        user_profile.save()
        user_profile.check_badges()
        user_profile.refresh_from_db()
        return redirect('profile', request.user.username)
    else:
        return HttpResponseRedirect(reverse('index'))

def watch_action(request):
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.action_movies_watched += 1
        user_profile.movies_watched += 1
        user_profile.save()
        user_profile.check_badges()
        user_profile.refresh_from_db()
        return redirect('profile', request.user.username)
    else:
        return HttpResponseRedirect(reverse('index'))


def watch_romance(request):
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.romance_movies_watched += 1
        user_profile.movies_watched += 1
        user_profile.save()
        user_profile.check_badges()
        user_profile.refresh_from_db()
        return redirect('profile', request.user.username)
    else:
        return HttpResponseRedirect(reverse('index'))


def watch_comedy(request):
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.comedy_movies_watched += 1
        user_profile.movies_watched += 1
        user_profile.save()
        user_profile.check_badges()
        user_profile.refresh_from_db()
        return redirect('profile', request.user.username)
    else:
        return HttpResponseRedirect(reverse('index'))

def recommend_movie_view(request):
    if request.method == "POST":
        user_movielist = request.POST.get("user_movielist")
        print(os.getcwd())
        #path = "static/csv"  # Creates path
        movies_file = pd.read_csv("static/csv/tmdb_5000_movies.csv")
        credits_file = pd.read_csv("static/csv/tmdb_5000_credits.csv")
        recommender = MovieRecommender(credits_file, movies_file)
        recommended_movies = recommender.recommend(user_movielist)
        display_movie = {"recommended_movies": recommended_movies}
        return render(request, "home/templates/recs/recommendList.html", display_movie)
    else:
        return render(request, "recs/addMovies.html")
>>>>>>> Stashed changes
