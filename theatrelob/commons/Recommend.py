import tmdbsimple as tmdb
import pandas as pd
from ast import literal_eval
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Function used to generate recommended movies using content based filtering
# Takes two csvfiles and a single movie. Will take a list of movies in the future.

def recommend(movieslist, creditsfile, moviesfile):
    creditsfile.columns = ['id', 'title', 'cast', 'crew']  # takes only id, title, cast, and crew columns
    moviesfile = moviesfile.merge(creditsfile, on="id")  # merges the dataframes using the id
    features = ["cast", "crew", "keywords", "genres"]  # build recommendation off these features

    for feature in features:  # converts data into usable structure. data is lists of strings until we convert
        moviesfile[feature] = moviesfile[feature].apply(literal_eval)

    moviesfile["director"] = moviesfile["crew"].apply(getdirector)  # gets directors
    features = ["cast", "keywords", "genres"]
    for feature in features:
        moviesfile[feature] = moviesfile[feature].apply(getlist)  # takes top 3 keywords of the features

    features = ['cast', 'keywords', 'director', 'genres']
    for feature in features:
        moviesfile[feature] = movies_df[feature].apply(cleandata)  # removes spaces and lowercases everything
    moviesfile["phrases"] = moviesfile.apply(prepvectorizer, axis=1)

    countvectorizer = CountVectorizer(stop_words="english")
    countmatrix = countvectorizer.fit_transform(moviesfile["phrases"])

    cosine_sim2 = cosine_similarity(count_matrix, count_matrix)

    moviesfile = moviesfile.reset_index()
    indices = pd.Series(moviesfile.index, index=moviesfile['title'])

    idx = indices[movieslist]
    simscore = list(enumerate(cosine_sim2[idx]))
    simscore = sorted(simscore, key=lambda x: x[1], reverse = True)
    simscore = simscore[1:11]

    moviesindices = [ind[0] for ind in simscore]
    movies = moviesfile["title"].iloc[movies_indices]
    return movies


# Loops over the crew for a movie to see if anyone is a director.
# Takes a crew and returns a person who is a director or none.
def getdirector(crew):
    for person in crew:
        if person["job"] == "Director":
            return person["name"]
        return np.nan


# Takes the top 3 elements of the list or the entire list if there are less than 3 elements.
# Takes a list and returns the top 3 elements of the entire list.
def getlist(x):
    if isinstance(x, list):
        names = [i["name"] for i in x]

        if len(names) > 3:
            names = names[:3]

        return names
    return []


# Function that cleans the instances by converting to lowercase and removing the spaces. Takes an instance of the data
def cleandata(row):
    if isinstance(row, list):
        return [str.lower(i.replace(" ", "")) for i in row]
    else:
        if isinstance(row, str):
            return str.lower(row.replace(" ", ""))
        else:
            return ""


# Function that prepares the data to be input into the vectorizer. Takes feature as input
def prepvectorizer(features):
    return ' '.join(features['keywords']) + ' ' + ' '.join(features['cast']) + ' ' + features[
        'director'] + ' ' + ' '.join(features['genres'])

