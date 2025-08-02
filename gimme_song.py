from flask import Flask, jsonify, redirect, request, send_from_directory
from flask_cors import CORS
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

sp_oauth = SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="user-read-playback-state",
    cache_path=".cache-gimmesong"
)

token_info = sp_oauth.get_cached_token()

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/authorize")
def authorize():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    token_info = sp_oauth.get_access_token(code)
    return "Autenticado con éxito. Ahora puedes usar Gimme Song!!"

@app.route("/current-song")
def current_song():
    global token_info
    if not token_info or sp_oauth.is_token_expired(token_info):
        token_info = sp_oauth.refresh_access_token(token_info["refresh_token"])

    sp = spotipy.Spotify(auth=token_info["access_token"])
    playback = sp.current_playback()

    # Si no hay reproducción activa, intenta recuperar la última canción pausada
    if not playback or not playback.get("item"):
        playback = sp.currently_playing()
        if not playback or not playback.get("item"):
            return jsonify({"status": "No music playing"})


    item = playback["item"]

    duration_ms = item["duration_ms"]
    progress_ms = playback["progress_ms"]

    def ms_to_min_sec(ms):
        minutes = ms // 60000
        seconds = (ms % 60000) // 1000
        return f"{minutes}:{seconds:02d}"

    return jsonify({
        "title": item["name"],
        "artist": ", ".join([a["name"] for a in item["artists"]]),
        "album": item["album"]["name"],
        "image": item["album"]["images"][0]["url"],
        "progress_ms": progress_ms,
        "duration_ms": duration_ms,
        "progress_text": ms_to_min_sec(progress_ms),
        "duration_text": ms_to_min_sec(duration_ms),
        "is_playing": playback.get("is_playing", False)
    })


if __name__ == "__main__":
    app.run(port=5000)
