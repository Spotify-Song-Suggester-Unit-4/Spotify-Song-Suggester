from json import JSONDecodeError
import requests
import time
from os import getenv

# Generate an access token
# authetication URL
AUTH_URL = 'https://accounts.spotify.com/api/token'
# POST
auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': getenv('SPOTIFY_CLIENT_ID'),
    'client_secret': getenv('SPOTIFY_CLIENT_SECRET'),
})
# convert the response to JSON
auth_response_data = auth_response.json()
# save the access token
access_token = auth_response_data['access_token']

# used for authenticating all API calls
headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}

# used for tracking genres
artist_genre = {}


def spotify_call(url):
    while True:
        request = requests.get(url, headers=headers)

        try:
            return request.json()

        except JSONDecodeError:
            wait = request.headers['retry-after']
            print(f"Waiting {wait} seconds for the API")
            time.sleep(int(wait))


def fetch_track(track_id):
    '''Fetches the spotify API response for a track'''
    url = f"https://api.spotify.com/v1/tracks/{track_id}"

    response = spotify_call(url)

    return response


def fetch_artist(artist_id):
    '''Requests the spotify API response for an artist'''
    url = f"https://api.spotify.com/v1/artists/{artist_id}"

    response = spotify_call(url)

    return(response)


def clean_genre(genre):
    '''Cleans up a genre's name for simplification'''
    # list of terms to remove
    removal_list = [
        "era",
        "vintage",
        "modern",
        "classic",
    ]

    # list of terms to automatically simplify to
    simplify_list = [
        "classical",
        "metal",
        "rock",
        "pop",
        "country",
        "opera",
        "jazz",
        "folk",
        "dance",
        "soundtrack",
        "modernism",
    ]

    genre_list = genre.split(" ")

    # return already simple genre names
    if len(genre_list) == 1:
        return genre

    # Start with the simplifications
    for word in genre_list:
        if word in simplify_list:
            return word

    new_genre_list = []

    for word in genre_list:
        if word not in removal_list:
            new_genre_list.append(word)

    new_genre = " ".join(new_genre_list).rstrip()

    return new_genre


def define_genre(genre_list):
    '''Decides the genre a particular artist falls under'''

    # Check if there is available genres
    if len(genre_list) == 0:
        return "unknown"

    # Find the simplest genre name
    genre_choices = [genre_list[0]]
    for genre in genre_list:
        genre_length = len(genre.split(" "))
        choice_length = len(genre_choices[0].split(" "))

        if genre_length < choice_length:
            genre_choices = [genre]

        elif genre_length == choice_length:
            genre_choices.append(genre)

    # Check for duplicates by converting to set and back
    genre_choices = list(set(genre_choices))

    # If there is only one choice, use that choice.
    return clean_genre(genre_choices[0])


def track_id_to_genre(track_id):
    track = fetch_track(track_id)

    try:
        artist_id = track["artists"][0]['id']

    except KeyError:
        print(f"No Artist listing for track {track_id}")
        print(track)
        return "unknown"

    artist = fetch_artist(artist_id)

    if artist_id in artist_genre:
        print("Reusing artist")
        return artist_genre[artist_id]

    try:
        genre_list = artist["genres"]

    except KeyError:
        print(f"No genre list found for artist {artist_id}")
        print(artist)
        return "unknown"

    genre = define_genre(genre_list)

    artist_genre[artist_id] = genre

    return genre


def test_data(length):
    '''Runs a test for defining genres in the data'''
    genres = []
    i = 0

    with open("data.csv", "r") as file:
        line = file.readline()  # headers
        line = file.readline().rstrip()  # first actual row

        while i < length and line != "":
            print(f"Checking Track {i}.", end="\r")
            try:
                id = line.split("]")[1].split(",")[5]

            except IndexError:
                genres.append("unknown")
                line = file.readline().rstrip()
                i += 1
                continue

            genre = track_id_to_genre(id)

            genres.append(genre)

            line = file.readline().rstrip()
            i += 1

    # genres = list(set(genres))
    return genres


if __name__ == "__main__":
    with open("genres.txt", "w") as file:
        file.write(",".join(test_data(170000)))
