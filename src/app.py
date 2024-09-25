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

    # Get selected dropdown values (with defaults)
    category = request.args.get('category', 'tracks')
    time_range = request.args.get('time_range', 'medium_term')
    limit = int(request.args.get('limit', '10'))

    items = []

    if category == 'tracks':
        results = sp.current_user_top_tracks(limit=limit, time_range=time_range)
        items = [
            {
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'image': track['album']['images'][0]['url'] if track['album']['images'] else None
            }
            for track in results['items']
        ]
    elif category == 'artists':
        results = sp.current_user_top_artists(limit=limit, time_range=time_range)
        items = [
            {
                'name': artist['name'],
                'image': artist['images'][0]['url'] if artist['images'] else None
            }
            for artist in results['items']
        ]

    return render_template(
        'stats.html',
        items=items,
        category=category,
        time_range=time_range,
        limit=limit
    )

if __name__ == "__main__":
    app.run(debug=True)
