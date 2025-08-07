from flask import request, jsonify, redirect, send_from_directory
from app import app
from app.services.spotify_service import get_spotify_data, init_spotify
import spotipy
from flask import request

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
    global token_info
    sp = spotipy.Spotify(auth=token_info["access_token"])

    spotify_data = get_spotify_data(sp, sp_oauth, token_info)

    if spotify_data and spotify_data.get("is_playing"):
        spotify_data["source"] = "spotify"
        return jsonify(spotify_data)
    
    

    # Si no se está reproduciendo nada, igual devuelvo los últimos datos conocidos
    return jsonify(spotify_data)
