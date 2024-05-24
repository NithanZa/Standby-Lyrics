import spotipy
from spotipy.oauth2 import SpotifyOAuth
from syncedlyrics import search as lrc_search
from dotenv import load_dotenv
from os import getenv

load_dotenv()

# Set up Spotify API credentials
SPOTIPY_CLIENT_ID = getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = 'https://example.com/callback'

# Authenticate with Spotify API
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope='user-read-currently-playing user-read-playback-state'
))


def get_track_details(queue_position: int, from_cache=False):
    artists = ""
    data = {}
    if queue_position < 0:
        raise ValueError("Queue position must not be less than 0")
    elif queue_position == 0:  # 0 is current
        playback_data = sp.current_playback()
        data = playback_data["item"]

    else:  # 1 is the one after the current song, in queue
        queue_data = sp.queue()
        data = queue_data["queue"][queue_position - 1]

    track = data["name"]
    for artist_info in data["artists"]:
        artists = artists + artist_info["name"] + ", "
    artists = artists[:-2]  # remove the extra comma and space
    image_url = data["album"]["images"][0]["url"]
    return track, artists, image_url


def get_queue_lyrics(queue_position: int, from_cache=False):
    track, artists, _ = get_track_details(queue_position, from_cache)
    return lrc_search(f"{track} {artists}")
