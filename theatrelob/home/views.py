import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
import json
import random
import tmdbsimple as tmdb
import requests
from .models import Integration, Movie, WatchedItem, Genre
from django.contrib.auth.decorators import login_required
import pandas as pd
import os
import secrets
from django.conf import settings
from .models import UserProfile, MovieRecommender
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Badge
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.views.decorators.csrf import csrf_exempt



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
    watched_items = WatchedItem.objects.filter(profile=profile).order_by('-date_watched').select_related('movie')

    movies = []
    #group the movies by the same day watched
    watched_items_grouped = []
    current_date = None
    for watched_item in watched_items:
        if current_date == None:
            current_date = watched_item.date_watched
            watched_items_grouped.append(watched_item)
        elif current_date == watched_item.date_watched:
            watched_items_grouped.append(watched_item)
        else:
            movies.append(watched_items_grouped)
            watched_items_grouped = []
            current_date = watched_item.date_watched
            watched_items_grouped.append(watched_item)
    
    movies.append(watched_items_grouped)
    # display the watched items
    return render(request, 'home/watchlist.html', {'watched_items': movies})

# Properply formatting the genre's name
def format_genre_name(genre):
        if genre.lower() == "tv movie":
            return "TV Movie"
        elif genre.lower() == "science fiction":
            return "Science Fiction"
        else:
            return genre.title()

@login_required(login_url='accounts/login/')
def remove_from_watchlist(request):
    # get the user's id
    user_id = request.user.id

    # get the user's profile
    profile = UserProfile.objects.get(user_id=user_id)

    # get the movie's id from the POST parameter
    movie_id = request.POST.get('movie_id', None)
    print("movie_id: ", movie_id)

    # get the movie
    m = Movie.objects.get(tmdb_id=movie_id)
    print("m: ", m)

    # remove the movie from the user's watchlist
    WatchedItem.objects.filter(profile=profile, movie=m).delete()

    # Update the number of movies watched
    profile.movies_watched -= 1
    
    profile.save()

    # redirect to the watchlist page
    return redirect('watchlist')

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
        if not Movie.objects.filter(tmdb_id=movie_id).exists():
            with open('secrets.json') as f:
                secrets = json.load(f)
                tmdb.API_KEY = secrets['tmdb_api_key']
            movie = tmdb.Movies(movie_id).info()

            poster_url = 'https://image.tmdb.org/t/p/w500' + movie['poster_path']
            
            m = Movie(tmdb_id=movie_id, title=movie['title'], description=movie['overview'], movie_poster_url=poster_url, release_date=movie['release_date'], runtime=movie['runtime'], 
                      rating=movie['vote_average'])
            m.save()
            
            # Correctly formatting and updating the generes
            for genre in m.genres.all():
                formatted_genre = format_genre_name(genre.name)
                profile.update_genres_watched(formatted_genre)
            
            # Save genres
            for genre in movie['genres']:
                genre_obj, _ = Genre.objects.get_or_create(name=genre['name'])
                m.genres.add(genre_obj)

            m.save()

        else:
            # get the movie
            m = Movie.objects.get(tmdb_id=movie_id)

        # add the movie to the user's watchlist

        # make sure the watched item doesn't already exist
        if WatchedItem.objects.filter(profile=profile, movie=m).exists():
            return redirect('watchlist')

        date = datetime.date.today()

        watched_item = WatchedItem(profile=profile, movie=m, date_watched=date)
        watched_item.save()

        # Update the number of movies watched
        profile.movies_watched += 1

        # Update genre count for each genre in the movie
        for genre in m.genres.all():
            profile.update_genres_watched(genre.name)
        

        profile.save()

        # redirect to the watchlist page
        return redirect('watchlist')


@login_required(login_url='accounts/login/')
def get_access_token(request):
    # get the user's id
    user_id = request.user.id
    # generate a random access token
    access_token = secrets.token_hex(16)


    # create an integration for the user
    # get the profile
    profile = UserProfile.objects.get(user_id=user_id)
    # get the date today and convert it to a string
    date = datetime.date.today()
    date = date.strftime("%Y-%m-%d")
    integration = Integration(profile=profile, name=date, access_token=access_token)
    integration.save()
    
    # refresh the page
    return redirect('profile/' + profile.user.username + '/')

@login_required(login_url='accounts/login/')
def delete_access_token(request):
    # get the user's id
    user_id = request.user.id

    # get the user's profile
    profile = UserProfile.objects.get(user_id=user_id)

    # get the access token from the POST parameter
    access_token = request.POST.get('access_token', None)

    if access_token is not None:
        # delete the integration
        integration = Integration.objects.get(profile=profile, access_token=access_token)
        integration.delete()
    
    # just refresh the page
    return redirect('profile/' + profile.user.username + '/')

@csrf_exempt
def api_search_and_add(request):
    # parse the body of the request as a json
    body = json.loads(request.body)

    # get the access token from the body
    access_token = body['access_token']

    # get the movie title from the POST parameter
    movie_title = body['movie_title']

    # find the integration with the access token
    integration = Integration.objects.get(access_token=access_token)

    # get the user's profile
    profile = integration.profile

    # search for the movie
    with open('secrets.json') as f:
        secrets = json.load(f)
        tmdb.API_KEY = secrets['tmdb_api_key']
    search = tmdb.Search()
    response = search.movie(query=movie_title)
    if(len(search.results) == 0):
        return HttpResponse(json.dumps({'success': False}), content_type="application/json")
    # get the movie id
    movie_id = search.results[0]['id']

    # check if the movie exists in the database
    if not Movie.objects.filter(tmdb_id=movie_id).exists():
        with open('secrets.json') as f:
            secrets = json.load(f)
            tmdb.API_KEY = secrets['tmdb_api_key']
        movie = tmdb.Movies(movie_id).info()

        poster_url = 'https://image.tmdb.org/t/p/w500' + movie['poster_path']
        
        m = Movie(tmdb_id=movie_id, title=movie['title'], description=movie['overview'], movie_poster_url=poster_url)
        m.save()
        
        # Correctly formatting and updating the generes
        for genre in m.genres.all():
            formatted_genre = format_genre_name(genre.name)
            profile.update_genres_watched(formatted_genre)
        
        # Save genres
        for genre in movie['genres']:
            genre_obj, _ = Genre.objects.get_or_create(name=genre['name'])
            m.genres.add(genre_obj)

        m.save()
    
    else:
        # get the movie
        m = Movie.objects.get(tmdb_id=movie_id)
    
    # add the movie to the user's watchlist

    # make sure the watched item doesn't already exist
    if WatchedItem.objects.filter(profile=profile, movie=m).exists():
        return HttpResponse(json.dumps({'success': "false", "ErrorMessage": "Already Watched"}), content_type='application/json')
    
    
    date = datetime.date.today()

    watched_item = WatchedItem(profile=profile, movie=m, date_watched=date)
    watched_item.save()

    # Update the number of movies watched
    profile.movies_watched += 1

    # Update genre count for each genre in the movie
    for genre in m.genres.all():
        profile.update_genres_watched(genre.name)
    

    profile.save()

    return HttpResponse(json.dumps({'success': "true"}), content_type='application/json')

def randomrec(request):

    adultFlag = True 

    with open('secrets.json') as f:
        secrets = json.load(f)
        tmdb.API_KEY = secrets['tmdb_api_key']

    latestMovieId = tmdb.Movies().latest()['id']

    while adultFlag == True:
        randomNum = random.randint(1, latestMovieId)

        while True:
            try:
                response = requests.get('https://api.themoviedb.org/3/movie/' + str(randomNum) + '?api_key=' + tmdb.API_KEY)
                response.raise_for_status()
                break
            except requests.exceptions.HTTPError as error:
                randomNum = random.randint(1, latestMovieId)
                continue

        movie   = tmdb.Movies(randomNum)
        movInfo = movie.info()

        if movInfo['adult'] == False:
            adultFlag = False

    movTitle = movInfo['title']
    poster   = movie.images()['posters']

    if len(poster) != 0:
        partPostUrl = poster[0]['file_path']
        fullPostUrl = 'https://image.tmdb.org/t/p/original' + partPostUrl
    else:
        fullPostUrl = 'https://www.smileysapp.com/emojis/wailing-emoji.png'

    return render(request, 'home/randomrec.html', {'movieTitle': movTitle, 'moviePoster': fullPostUrl}) 

def theaters(request):
    return render(request, 'home/theaters.html')

@login_required
# Handles the home page view
def home(request):
    # Renders the homepage template and returns it as an HTTP response
    return render(request, 'profiles/home.html')

# This is to render the login page
class CustomLoginView(LoginView):
    login_page = 'home/login.html'

# Handles the logout view
def logout_view(request):
    # Calls Django's logout function and logs the user out
    logout(request)
    # Redirects the user back to the main page
    return redirect('index')

# Handles the registration view
def register(request):
    # Checks if the request method is form submission
    if request.method == 'POST':
        # Initializes a UserCreationForm with the given data
        form = UserCreationForm(request.POST)
        # Validates the form
        if form.is_valid():
            # Saves the form
            user = form.save()
            # Check if a UserProfile already exists for the user
            if not UserProfile.objects.filter(user=user).exists():
                # Creates the user's profile for the new user
                UserProfile.objects.create(user=user)
            # Logs the user in
            login(request, user)
            # Redirects the user to the homepage
            return redirect('index')
    else:
        # Initializes an empty UserCreationForm if there's no request method
        form = UserCreationForm()
    
    # Setting the form's data to the form variable to be used in a template
    context = {'form' : form}
    # Renders the registratoin template with the form data and returns it as an HTTP response
    return render(request, 'profile/register.html', context)

# Handldes the user's profile view
def profile(request, username):
    # Validates the user and checks if the requested username matches the logged in username
    if request.user.is_authenticated and request.user.username == username:
        # Get the data correlating to the user
        user_profile = UserProfile.objects.get(user=request.user)
        integrations = Integration.objects.filter(profile=user_profile)
        print(integrations)
        # Updates the user's badges
        user_profile.check_badges()
        # Refreshes the user's profile to reflect any changes
        user_profile.refresh_from_db() 

        # Setting the user_profile's data to the profile variable to be used in a template
        context = {'profile': user_profile, 'integrations': integrations}
        # Renders the profile template with the user's profile data and returns it as an HTTP response
        return render(request, 'profile/profile.html', context)
    else:
        # Redirect the user back to the homepage if the user isn't validated
        return HttpResponseRedirect(reverse('index'))

# Handles the list of badges views
def badge_list(request):
    # Validates the user
    if request.user.is_authenticated:
        # Get the badge objects
        badges = Badge.objects.all()
        # Get the user's profile data
        profile = UserProfile.objects.get(user=request.user)

        # Setting the badge's and profile's data to the badges and profile variables to be used in a template
        context = {'badges': badges, 'profile': profile}
        # Renders the badge list template with the user's profile and badge data and returns it as an HTTP response
        return render(request, 'profile/badge_list.html', context)
    else:
        # Redirect the user back to the homepage if the user isn't validated
        return HttpResponseRedirect(reverse('index'))

# Creates the badges
def create_badges(request):
    # Defines the badge data as a list of dictionaries containing each badge info
    badges_data = [
        {
            'name': '10 Movies Watched',
            'description': 'Watch 10 movies.',
            'type': 'movies_watched',
            'requirement': 10
        },
        {
            'name': '20 Movies Watched',
            'description': 'Watch 20 movies.',
            'type': 'movies_watched',
            'requirement': 20
        },
        {
            'name': 'Genre Enthusiast',
            'description': 'Watch movies from 5 different genres.',
            'type': 'genres_watched',
            'requirement': 5
        },
        {
            'name': "Dom Toretto's Family",
            'description': 'Watch 5 Action Movies.',
            'type': 'genre',
            'genre': 'Action',
            'requirement': 5
        },
        {
            'name': "Indiana Jone's Party",
            'description': 'Watch 5 Adventure Movies.',
            'type': 'genre',
            'genre': 'Adventure',
            'requirement': 5
        },
        {
            'name': "Micky's Clubhouse",
            'description': 'Watch 5 Animation Movies.',
            'type': 'genre',
            'genre': 'Animation',
            'requirement': 5
        },
        {
            'name': "McLovin's BFF",
            'description': 'Watch 5 Comedy Movies.',
            'type': 'genre',
            'genre': 'Comedy',
            'requirement': 5
        },
        {
            'name': "John Wick's Hitlist",
            'description': 'Watch 5 Crime Movies.',
            'type': 'genre',
            'genre': 'Crime',
            'requirement': 5
        },
        {
            'name': "Tiger King's Lil Kitten",
            'description': 'Watch 5 Documentary Movies.',
            'type': 'genre',
            'genre': 'Documentary',
            'requirement': 5
        },
        {
            'name': "Rocky's Opponent",
            'description': 'Watch 5 Drama Movies.',
            'type': 'genre',
            'genre': 'Drama',
            'requirement': 5
        },
        {
            'name': "Shrek Is love Shrek Is Life",
            'description': 'Watch 5 Family Movies.',
            'type': 'genre',
            'genre': 'Family',
            'requirement': 5
        },
        {
            'name': "Lord Voldemort's Follower",
            'description': 'Watch 5 Fantasy Movies.',
            'type': 'genre',
            'genre': 'Fantasy',
            'requirement': 5
        },
        {
            'name': "Apollo 13's Hidden Crew Member",
            'description': 'Watch 5 History Movies.',
            'type': 'genre',
            'genre': 'History',
            'requirement': 5
        },
        {
            'name': "Michael Myer's Next Target",
            'description': 'Watch 5 Horror Movies.',
            'type': 'genre',
            'genre': 'Horror',
            'requirement': 5
        },
        {
            'name': "Dorothy's Friend",
            'description': 'Watch 5 Music Movies.',
            'type': 'genre',
            'genre': 'Music',
            'requirement': 5
        },
        {
            'name': "???",
            'description': 'Watch 5 Mystery Movies.',
            'type': 'genre',
            'genre': 'Mystery',
            'requirement': 5
        },
        {
            'name': 'Fifty Shades of Software Sweethearts',
            'description': 'Watch 5 Romance Movies.',
            'type': 'genre',
            'genre': 'Romance',
            'requirement': 5
        },
        {
            'name': "Blade Runner's Cyberpunk Circle",
            'description': 'Watch 5 Science Fiction Movies.',
            'type': 'genre',
            'genre': 'Science Fiction',
            'requirement': 5
        },
        {
            'name': "Parsite's Cunning Crew",
            'description': 'Watch 5 Thriller Movies.',
            'type': 'genre',
            'genre': 'Thriller',
            'requirement': 5
        },
        {
            'name': 'Couch Potato',
            'description': 'Watch 5 TV Movie Movies.',
            'type': 'genre',
            'genre': 'TV Movie',
            'requirement': 5
        },
        {
            'name': 'American Snipers Enemy',
            'description': 'Watch 5 War Movies.',
            'type': 'genre',
            'genre': 'War',
            'requirement': 5
        },
        {
            'name': 'The Elite Gunslinger',
            'description': 'Watch 5 Western Movies.',
            'type': 'genre',
            'genre': 'Western',
            'requirement': 5
        },
    ]

    # Iterating through the badge data
    for badge_data in badges_data:
        # Creates the badge object or get it if it already exists
        Badge.objects.get_or_create(
            # Obtaining the name, description, type, genre, and requirement criteras
            name=badge_data['name'],
            description=badge_data['description'],
            badge_type=badge_data.get('type'),
            genre=badge_data.get('genre', ''),
            requirement=badge_data.get('requirement', 0),
        )

    # Send a reponse to indicate that the badges have been created 
    return HttpResponse("Badges created!")

# Resets the user's badge data
def reset_user_badges(request):
    # Validates the user
    if request.user.is_authenticated:
        # Get the user's profile data
        user_profile = UserProfile.objects.get(user=request.user)

        # Clearing the user's badge data
        user_profile.badges.clear()
        user_profile.movies_watched = 0
        user_profile.action_movies_watched = 0
        user_profile.adventure_movies_watched = 0
        user_profile.animation_movies_watched = 0
        user_profile.comedy_movies_watched = 0
        user_profile.crime_movies_watched = 0
        user_profile.documentary_movies_watched = 0
        user_profile.drama_movies_watched = 0
        user_profile.family_movies_watched = 0
        user_profile.fantasy_movies_watched = 0
        user_profile.history_movies_watched = 0
        user_profile.horror_movies_watched = 0
        user_profile.music_movies_watched = 0
        user_profile.mystery_movies_watched = 0
        user_profile.romance_movies_watched = 0
        user_profile.science_fiction_movies_watched = 0
        user_profile.thriller_movies_watched = 0
        user_profile.tv_movie_movies_watched = 0
        user_profile.war_movies_watched = 0
        user_profile.western_movies_watched = 0
        user_profile.save()

        # Redirects the user back to the profile page with the specified username
        return HttpResponseRedirect(reverse('profile', args=[request.user.username]))
    else:
        # Redirects the user back to the homepage
        return HttpResponseRedirect(reverse('index'))

# Deletes the badges
def delete_badges(request):
    # Deletes all the badge objects from the database
    Badge.objects.all().delete()
    # Send a reponse to indicate that the badges have been deleted 
    return HttpResponse("Badges deleted!")

def recommend_movie_view(request):
    if request.method == "POST":
        user_movielist = request.POST.get("user_movielist")
        csvmovies_path = os.path.join(os.path.dirname(__file__), 'tmdb_5000_movies.csv')
        csvcredits_path = os.path.join(os.path.dirname(__file__), 'tmdb_5000_credits.csv')
        movies_file = pd.read_csv(csvmovies_path)
        credits_file = pd.read_csv(csvcredits_path)
        recommender = MovieRecommender(credits_file, movies_file)
        recommended_movies = recommender.recommend(user_movielist)
        recommended_movies_plots = recommender.plotrec(user_movielist)
        rec_movies = []
        rec_movies_plots = []
        search = tmdb.Search()
        if recommended_movies is None:
            return render(request, "recs/movieNotFound.html")
        for title in recommended_movies:
            with open('secrets.json') as f:
                secrets = json.load(f)
                tmdb.API_KEY = secrets['tmdb_api_key']

            # Searches for movie and gets the id of the top result
            response = search.movie(query=title)

            movie_id = search.results[0]['id']
            # check if the movie exists in the database
            if not Movie.objects.filter(tmdb_id=movie_id).exists():
                # Gets the movie info using the movie id
                movie = tmdb.Movies(movie_id).info()

                # Gets the poster url
                poster_url = 'https://image.tmdb.org/t/p/w500' + movie['poster_path']
                m = Movie(tmdb_id=movie_id, title=movie['title'], description=movie['overview'],
                          movie_poster_url=poster_url)

                m.save()
            else:
                # get the movie
                m = Movie.objects.get(tmdb_id=movie_id)
                rec_movies.append(m)

        for title in recommended_movies_plots:
            with open('secrets.json') as f:
                secrets = json.load(f)
                tmdb.API_KEY = secrets['tmdb_api_key']

            # Searches for movie and gets the id of the top result
            response = search.movie(query=title)

            movie_id = search.results[0]['id']
            # check if the movie exists in the database
            if not Movie.objects.filter(tmdb_id=movie_id).exists():
                # Gets the movie info using the movie id
                movie = tmdb.Movies(movie_id).info()

                # Gets the poster url
                poster_url = 'https://image.tmdb.org/t/p/w500' + movie['poster_path']
                m = Movie(tmdb_id=movie_id, title=movie['title'], description=movie['overview'],
                          movie_poster_url=poster_url)

                m.save()

                genres_list = []
                for genre in movie['genres']:
                    genre_obj, _ = Genre.objects.get_or_create(name=genre['name'])
                    genres_list.append(genre_obj)

                m.genres.set(genres_list)

                m.save()

                for genre in m.genres.all():
                    formatted_genre = format_genre_name(genre.name)
            else:
                # get the movie
                m = Movie.objects.get(tmdb_id=movie_id)
                rec_movies_plots.append(m)

        display_movie = {"rec_movies": rec_movies,
                         "rec_movies_plots": rec_movies_plots}
        return render(request, "recs/recommendList.html", display_movie)
    else:
        return render(request, "recs/addMovies.html")


# For searching and adding movies to the movie list
def movie_search_add(request):
    if request.method == "POST":
        # Get the movie to add in a string
        user_movie_add = request.POST.get("user_movie_add")
        user_movie_add = str(user_movie_add)
        # get the user's id
        user_id = request.user.id

        # get the user's profile
        profile = UserProfile.objects.get(user_id=user_id)

        search = tmdb.Search()

        if user_movie_add is not None:
            with open('secrets.json') as f:
                secrets = json.load(f)
                tmdb.API_KEY = secrets['tmdb_api_key']

            # Searches for movie and gets the id of the top result
            response = search.movie(query=user_movie_add)
            movie_id = search.results[0]['id']

            # check if the movie exists in the database
            if not Movie.objects.filter(tmdb_id=movie_id).exists():
                # Gets the movie info using the movie id
                movie = tmdb.Movies(movie_id).info()

                # Gets the poster url
                poster_url = 'https://image.tmdb.org/t/p/w500' + movie['poster_path']
                m = Movie(tmdb_id=movie_id, title=movie['title'], description=movie['overview'], movie_poster_url=poster_url)

                m.save()
                
                # Save every genre from tmdb database
                genres_list = []
                for genre in movie['genres']:
                    genre_obj, _ = Genre.objects.get_or_create(name=genre['name'])
                    genres_list.append(genre_obj)

                # Add genres to the movie
                m.genres.set(genres_list)

                # Save the movie with genres
                m.save()

            else:
                # get the movie
                m = Movie.objects.get(tmdb_id=movie_id)

            # add the movie to the user's watchlist
            date = datetime.date.today()

            watched_item = WatchedItem(profile=profile, movie=m, date_watched=date)
            watched_item.save()

            # Correctly formatting the genre names and updates the count for each genre
            for genre in m.genres.all():
                formatted_genre = format_genre_name(genre.name)
                profile.update_genres_watched(formatted_genre)

            # Updates the number of movies watched
            profile.movies_watched += 1
            profile.save()

            # redirect to the success page
            return render(request, "profile/addedMovie.html")
    else:
        return render(request, "profile/searchAdd.html")











