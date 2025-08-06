from flask import request, jsonify, redirect, send_from_directory
from app import app
from app.services.spotify_service import get_spotify_data, init_spotify
from app.services.youtube_service import get_youtube_data
import spotipy


sp_oauth, token_info = init_spotify()

last_platform = "spotify"  # ← Global variable

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/authorize")
def authorize():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route("/callback")
def callback():
    global token_info
    code = request.args.get("code")
    token_info = sp_oauth.get_access_token(code)
    return "Autenticado con éxito. Ahora puedes usar Gimme Song!!"

@app.route("/current-song")
def current_song():
    global token_info, last_platform
    sp = spotipy.Spotify(auth=token_info["access_token"])

    spotify_data = get_spotify_data(sp, sp_oauth, token_info)
    if spotify_data and spotify_data.get("is_playing"):
        last_platform = "spotify"
        spotify_data["source"] = "spotify"
        return jsonify(spotify_data)

    youtube_data = get_youtube_data()
    if youtube_data and youtube_data.get("is_playing"):
        last_platform = "youtube"
        youtube_data["source"] = "youtube"
        return jsonify(youtube_data)

    # Si ninguna está activa, devuelvo la última conocida
    if last_platform == "spotify":
        return jsonify(spotify_data)
    else:
        return jsonify(youtube_data)
