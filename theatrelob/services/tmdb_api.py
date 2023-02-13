
import json
import tmdbsimple as tmdb
#read secrets.json file one dir up
with open('../secrets.json') as f:
    secrets = json.load(f)
    tmdb.API_KEY = secrets['tmdb_api_key']

