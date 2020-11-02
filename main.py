import typing

import spotipy
from spotipy.oauth2 import SpotifyOAuth


#  Create a spotify instance with user_id
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id="placeholder",
        client_secret="placeholder",
        redirect_uri="http://example.com/callback/",
        scope="user-library-read",
    )
)


running = True


def convert_ms_to_minutes(ms: int):
    """
    Function that converts ms to minutes and seconds
    :param ms: milliseconds
    :return: formatted string
    """

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


def show_recommendations_for_artist(artist: typing.Dict):
    """
    API call that gets recommendations based on the artist
    :param artist: string
    :return: A list of recommendations
    """
    songs = []
    artist_recommendations = sp.recommendations(seed_artists=[artist["id"]], limit=50)
    for i, entry in enumerate(artist_recommendations["tracks"]):
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


# Main loop
while running:
    name = artist_input()
    results = sp.search(q="artist:" + name, type="artist")
    items = results["artists"]["items"]
    if len(items) > 0:
        selected_artist = items[0]
        recommendations = show_recommendations_for_artist(selected_artist)
        selected_song = recommendation_input()
        get_song_info(recommendations, selected_song)
        break
    else:
        print("Artist not found, try again")
