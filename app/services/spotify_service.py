import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from app.utils.time import ms_to_min_sec

def init_spotify():
    sp_oauth = SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope="user-read-playback-state",
        cache_path=".cache-gimmesong"
    )
    token_info = sp_oauth.get_cached_token()
    return sp_oauth, token_info

def get_spotify_data(sp, sp_oauth, token_info):
    if not token_info or sp_oauth.is_token_expired(token_info):
        token_info = sp_oauth.refresh_access_token(token_info["refresh_token"])
        sp = spotipy.Spotify(auth=token_info["access_token"])

    playback = sp.current_playback()
    if not playback or not playback.get("item") or not playback.get("is_playing", False):
        return None

    item = playback["item"]
    duration_ms = item["duration_ms"]
    progress_ms = playback["progress_ms"]

    return {
        "title": item["name"],
        "artist": ", ".join([a["name"] for a in item["artists"]]),
        "album": item["album"]["name"],
        "image": item["album"]["images"][0]["url"],
        "progress_ms": progress_ms,
        "duration_ms": duration_ms,
        "progress_text": ms_to_min_sec(progress_ms),
        "duration_text": ms_to_min_sec(duration_ms),
        "is_playing": playback.get("is_playing", False)
    }
