# get_current_song.py

import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# Cargar variables desde .env
load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="user-read-playback-state",
    cache_path=".cache-gimmesong"
))

current = sp.current_playback()

if current and current["is_playing"]:
    song = current["item"]
    print("🎵 Título:", song["name"])
    print("🎤 Artista:", ", ".join([a["name"] for a in song["artists"]]))
    print("💿 Álbum:", song["album"]["name"])
    print("⏱️ Duración:", round(song["duration_ms"] / 1000), "segundos")
    print("📍 Progreso:", round(current["progress_ms"] / 1000), "segundos")
else:
    print("No hay música reproduciéndose.")
