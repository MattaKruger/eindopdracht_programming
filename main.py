import logging

import spotipy
from spotipy.oauth2 import SpotifyOAuth

logger = logging.getLogger('examples.artist_recommendations')
logging.basicConfig(level='INFO')


#  Create a spotify instance with user_id
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="8f67eeced8ae42e18ee86373d102a283",
                                               client_secret="7405c0937da6421dad1a40860ecbf9ee",
                                               redirect_uri="http://example.com/callback/",
                                               scope="user-library-read"))


#  Returns an input instance
def artist_input():
    return input("Enter your favorite artist and get recommendations: ")


def get_artist(name):
    """
    API call that finds artists
    :param name:
    :return: artist name
    """
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        return items[0]
    else:
        logger.info('Artist not found ')


def show_recommendations_for_artist(artist):
    """
    API call that gets recommendations based on the artist
    :param artist: string
    :return: A list of recommendations
    """
    songs = []
    results = sp.recommendations(seed_artists=[artist['id']], limit=50)
    for track in results['tracks']:
        logger.info('Recommendation: %s - %s', track['name'], track['artists'][0]['name'])
        songs.append({'song': track['name'], 'artist': track['artists'][0]['name']})
    return songs


selected_artist = get_artist(artist_input())

recommendations = show_recommendations_for_artist(selected_artist)
