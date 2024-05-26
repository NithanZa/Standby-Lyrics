import time

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from syncedlyrics import search as lrc_search
from dotenv import load_dotenv
from os import getenv
from time import sleep
from time import time as now

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

cache = [()] * 5
playback_cache = {}  # track, artists, image_url, playback ms, recorded ms


def get_track_details(queue_position: int, from_cache=False):
    if from_cache:
        return cache[queue_position]
    else:
        artists = ""
        if queue_position < 0:
            raise ValueError("Queue position must not be less than 0")
        elif queue_position == 0:  # 0 is previous
            recent_data = sp.current_user_recently_played()
            data = recent_data["items"][0]
        elif queue_position == 1:  # 1 is current
            return get_playback_details()  # cache already gets updated in this call
        else:  # 2+ are the next songs
            queue_data = sp.queue()
            data = queue_data["queue"][queue_position - 2]

        track = data["name"]
        for artist_info in data["artists"]:
            artists = artists + artist_info["name"] + ", "
        artists = artists[:-2]  # remove the extra comma and space
        cache[queue_position] = (track, artists)
        return track, artists


def get_queue_lyrics(queue_position: int, from_cache=False):
    track_details = get_track_details(queue_position, from_cache)
    track = track_details[0]
    artists = track_details[1]
    return lrc_search(f"{track} {artists}")


def get_playback_details(from_cache=False):
    global playback_cache
    if from_cache:
        return playback_cache
    else:
        playback_data = sp.current_user_recently_played()
        track = playback_data["item"]["name"]
        artists = ""
        for artist_info in playback_data["item"]["artists"]:
            artists = artists + artist_info["name"] + ", "
        artists = artists[:-2]  # remove the extra comma and space
        recorded_ms = round(now() * 1000)
        playback_ms = playback_data["progress_ms"]
        image_url = playback_data["item"]["album"]["images"][0]["url"]
        playback_data = {
            "track": track,
            "artists": artists,
            "recorded_ms": recorded_ms,
            "playback_ms": playback_ms,
            "image_url": image_url
        }
        playback_cache = playback_data
        cache[1] = (track, artists)
        return playback_data


# def update_cache():
#     while True:
#         time.sleep(1)
