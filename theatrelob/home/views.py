import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
import json
import random
import tmdbsimple as tmdb
from .models import Integration, Movie, WatchedItem
import requests
from .models import Movie, UserProfile, WatchedItem
from django.contrib.auth.decorators import login_required
#
from django.shortcuts import render, get_object_or_404
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Badge
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView



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

        m = Movie(title=movie['title'], description=movie['overview'], movie_poster_url=poster_url, tmdb_id=movie['id'])
        batch_of_three_movies.append(m)
        if len(batch_of_three_movies) == 3:
            list_of_movies.append(batch_of_three_movies)
            batch_of_three_movies = []

    # get image url
    return render(request, 'home/index.html', {'movies': list_of_movies})

@login_required(login_url='accounts/login/')
def watchlist(request):
    # retrieve all watched items from the database belonging to the user
    # display them on the page
    # get the user's id
    user_id = request.user.id

    # get the user's profile
    profile = UserProfile.objects.get(user_id=user_id)
    # get the user's watched items
    watched_items = WatchedItem.objects.filter(profile=profile)
    
    # display the watched items
    return render(request, 'home/watchlist.html', {'watched_items': watched_items})

@login_required(login_url='accounts/login/')
def add_to_watchlist(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # get the user's id
    user_id = request.user.id

    # get the user's profile
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

    adultFlag = True 

    with open('secrets.json') as f:
        secrets = json.load(f)
        tmdb.API_KEY = secrets['tmdb_api_key']

    latestMovieId = tmdb.Movies().latest()['id']

    while adultFlag == True:
        randomNum = random.randint(1, latestMovieId)
        print('randomNum is', randomNum)  # Debug statement

        while True:
            try:
                response = requests.get('https://api.themoviedb.org/3/movie/' + str(randomNum) + '?api_key=' + tmdb.API_KEY)
                response.raise_for_status()
                break
            except requests.exceptions.HTTPError as error:
                randomNum = random.randint(1, latestMovieId)
                print('404 error')  # Debug statement
                continue

        movie   = tmdb.Movies(randomNum)
        movInfo = movie.info()

        if movInfo['adult'] == False:
            adultFlag = False
        else:
            print('Adult film!') # Debug statement

    movTitle = movInfo['title']
    poster   = movie.images()['posters']

    if len(poster) != 0:
        partPostUrl = poster[0]['file_path']
        fullPostUrl = 'https://image.tmdb.org/t/p/original' + partPostUrl
    else:
        fullPostUrl = 'https://www.smileysapp.com/emojis/wailing-emoji.png'

    return render(request, 'home/randomrec.html', {'movieTitle': movTitle, 'moviePoster': fullPostUrl}) 

def theaters(request):
    temp = 0;
    return render(request, 'home/theaters.html')

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