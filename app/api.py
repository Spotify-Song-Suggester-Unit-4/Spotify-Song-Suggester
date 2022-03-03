import requests
from os import getenv

def parse_input(song_name_input, artist_input):
    '''
    Receives raw text from both song text boxes and returns track id using the api to parse
    '''
    # Generate an access token (every time function is called)
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

    #strips leading whitespace and replaces internal whitespace with % for api query
    song_name_input = song_name_input.strip().replace(" ", "%")
    artist_input = artist_input.strip().replace(" ", "%")

    # GET request to get the track id given song and artist
    # returns top 1 result
    api_response = requests.get(
        f'''https://api.spotify.com/v1/search?query=track:{song_name_input}
        +artist:{artist_input}&type=track&limit=1''', headers=headers).json()

    input_id = api_response['tracks']['items'][0]['id']

    return input_id
    