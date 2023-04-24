import tmdbsimple as tmdb
import random
import requests
import json

def randomRecGenerator():
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
        return movTitle, fullPostUrl
    else:
        fullPostUrl = 'https://www.smileysapp.com/emojis/wailing-emoji.png'
        return movTitle, fullPostUrl