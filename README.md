# Spotify Statistics Web App

This is a Flask-based web application that allows users to view their Spotify statistics such as their top tracks, top artists, and recently played tracks using the Spotify API. Users can filter results by time range and number of results and see useful information such as play counts and listening times.

## Features
- **Top Tracks/Artists:** View your most listened-to tracks and artists.
- **Recently Played:** Display a list of recently played tracks.
- **Hover Data:** See play counts for individual tracks and total listening time for artists when hovering over a card.
- **Dynamic Dropdowns:** Filter data by time range and result count (e.g., Top 10, Top 25, Top 50).
- **Responsive Grid Layout:** Cards showing track/artist information with album/artist art.

## Prerequisites
Before running the application, ensure you have the following installed:
- Python 3.x
- Pip (Python package installer)
- A Spotify Developer account with access to the [Spotify Web API](https://developer.spotify.com/documentation/web-api/).

## Setup

### 1. Clone the Repository
```bash
git clone https://github.com/timothja/SpotifyStats.git
cd SpotifyStats
```

### 2. Install Required Packages
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

### 3. Set Up Spotify Developer Credentials

Go to the Spotify Developer Dashboard.
Create an app to obtain your CLIENT_ID and CLIENT_SECRET.
Set your Redirect URI to http://127.0.0.1:5000/callback in the app settings.

### 4. Create a .env File
Create a `.env` file in the root directory of the project and add the following lines:
```bash
SPOTIPY_CLIENT_ID='your_client_id'
SPOTIPY_CLIENT_SECRET='your_client_secret'
SPOTIPY_REDIRECT_URI='http://localhost:5000/callback'
```
Replace `'your_client_id'` and `'your_client_secret'` with your Spotify Developer client ID and client secret, respectively.

### 5. Run the Application
```bash
python3 ./src/app.py
```

Open a web browser and navigate to `http://localhost:5000` to view the application.


## Screenshots


![Top Tracks](https://user-images.githubusercontent.com/6625384/134773073-1b3b3b3b-1b3b-4b3b-8b3b-1b3b3b3b3b3b.png)

![Top Artists](https://user-images.githubusercontent.com/6625384/134773076-1b3b3b3b-1b3b-4b3b-8b3b-1b3b3b3b3b3b.png)


## Folder Structure
``` bash
.
├── LICENSE # MIT License
├── README.md # This file
├── requirements.txt # Required Python packages
└── src
    ├── app.py # Main application file
    ├── static # Static files (CSS, JS, images)
    │   └── styles.css
    └── templates # HTML templates
        ├── base.html
        ├── index.html
        ├── recently_played.html
        └── tops.html

```