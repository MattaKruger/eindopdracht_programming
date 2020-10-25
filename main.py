import typing

import spotipy
from spotipy.oauth2 import SpotifyOAuth


#  Create a spotify instance with user_id
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id="8f67eeced8ae42e18ee86373d102a283",
        client_secret="7405c0937da6421dad1a40860ecbf9ee",
        redirect_uri="http://example.com/callback/",
        scope="user-library-read",
    )
)


def convert_ms_to_minutes(ms: int):
    minutes = int((ms / (1000 * 60)) % 60)
    seconds = int((ms / 1000) % 60)
    return "minutes: {} and {} seconds".format(minutes, seconds)


def artist_input():
    return input("Enter your favorite artist and get recommendations: ")


def recommendation_input():
    return int(input("Select a song 0 through 49: "))


def get_song_info(songs: typing.List, index: int):
    # Generation expression that searches list of dicts based on index
    song = next(item for item in songs if item["id"] == index)
    print("You have selected: {} - {}".format(song["song"], song["artist"]))

    # API call that gets track info based on the songs uri
    song_info = sp.track(song["uri"])

    popularity = song_info["popularity"]
    duration = convert_ms_to_minutes(song_info["duration_ms"])
    album_type = song_info["album"]["album_type"]

    print(
        "Popularity: {}, duration: {}, type: {}".format(
            popularity, duration, album_type
        )
    )


def get_artist(name: str):
    """
    API call that finds artists or
    :param name:
    :return: artist name
    """
    results = sp.search(q="artist:" + name, type="artist")
    items = results["artists"]["items"]
    if len(items) > 0:
        return items[0]
    else:
        print("Artist not found, try again please")


def show_recommendations_for_artist(artist: typing.Dict):
    """
    API call that gets recommendations based on the artist
    :param artist: string
    :return: A list of recommendations
    """
    songs = []
    results = sp.recommendations(seed_artists=[artist["id"]], limit=50)
    for i, entry in enumerate(results["tracks"]):
        print(
            "Recommendation: {}: {} - {}".format(
                i, entry["name"], entry["artists"][0]["name"]
            )
        )
        songs.append(
            {
                "id": i,
                "song": entry["name"],
                "artist": entry["artists"][0]["name"],
                "uri": entry["uri"],
            }
        )
    return songs


selected_artist = get_artist(artist_input())

recommendations = show_recommendations_for_artist(selected_artist)

if __name__ == "__main__":
    get_song_info(recommendations, recommendation_input())
