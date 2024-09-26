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
    scope="user-top-read user-read-recently-played"
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info
    return redirect(url_for('tops'))

@app.route('/tops')
def tops():
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
        # Get top tracks
        results = sp.current_user_top_tracks(limit=limit, time_range=time_range)
        # Calculate play count and total time listened from recently played
        recent_tracks = sp.current_user_recently_played(limit=50)
        play_counts = calculate_play_counts(recent_tracks)

        for track in results['items']:
            play_count = play_counts.get(track['id'], 0)

            items.append({
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'image': track['album']['images'][0]['url'] if track['album']['images'] else None,
                'play_count': play_count,
            })

    elif category == 'artists':
        # Get top artists
        results = sp.current_user_top_artists(limit=limit, time_range=time_range)

        # Calculate total listening time for each artist based on recent playback data
        recent_tracks = sp.current_user_recently_played(limit=50)
        artist_listen_times = calculate_artist_listen_times(recent_tracks)

        for artist in results['items']:
            play_count = artist_listen_times.get(artist['id'], 0)
            items.append({
                'name': artist['name'],
                'image': artist['images'][0]['url'] if artist['images'] else None,
                'play_count': play_count,
            })

    return render_template(
        'tops.html',
        items=items,
        category=category,
        time_range=time_range,
        limit=limit
    )

@app.route('/recently-played')
def recently_played():
    token_info = session.get('token_info')
    if not token_info:
        return redirect('/')

    sp = spotipy.Spotify(auth=token_info['access_token'])

    # Get recently played tracks
    recent_tracks = sp.current_user_recently_played(limit=50)

    # Prepare the data to pass to the template
    items = []
    for item in recent_tracks['items']:
        track = item['track']
        played_at = item['played_at']
        items.append({
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'image': track['album']['images'][0]['url'] if track['album']['images'] else None,
            'played_at': played_at
        })

    return render_template(
        'recently_played.html',
        items=items
    )


def calculate_play_counts(recent_tracks):
    play_counts = {}
    for track in recent_tracks['items']:
        track_id = track['track']['id']
        if track_id not in play_counts:
            play_counts[track_id] = 0
        play_counts[track_id] += 1
    return play_counts

def calculate_artist_listen_times(recent_tracks):
    play_counts = {}
    for item in recent_tracks['items']:
        track = item['track']
        artist_id = track['artists'][0]['id']

        if artist_id not in play_counts:
            play_counts[artist_id] = 0
        play_counts[artist_id] += 1
    return play_counts


if __name__ == "__main__":
    app.run(debug=True)
