from flask import Flask, redirect, url_for, session, request, render_template
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = "random_secret_key"
app.config['SESSION_COOKIE_NAME'] = 'spotify-login-session'


sp_oauth = SpotifyOAuth(
    client_id=os.getenv('SPOTIPY_CLIENT_ID'),
    client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
    redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI'),
    scope="user-top-read"
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info
    return redirect(url_for('stats'))

@app.route('/stats')
def stats():
    token_info = session.get('token_info')
    if not token_info:
        return redirect('/')
    
    sp = spotipy.Spotify(auth=token_info['access_token'])
    top_tracks = sp.current_user_top_tracks(limit=10)
    return render_template('stats.html', tracks=top_tracks['items'])

if __name__ == "__main__":
    app.run(debug=True)
