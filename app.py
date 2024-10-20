# Import necessary libraries and modules from Flask, requests, SQLite, and datetime
from flask import Flask, render_template, request, jsonify
import requests
import sqlite3
from datetime import datetime
import os

# Initialize the Flask app
app = Flask(__name__)

# Spotify API Credentials for authenticating requests
SPOTIFY_CLIENT_ID = 'bc93a10a093245ceb6d8610f0825ee86'
SPOTIFY_CLIENT_SECRET = '6f25a2ad278c4d04bb9b1f109be7f03d'

# YouTube API Key for accessing the YouTube Data API
YOUTUBE_API_KEY = "AIzaSyAr14gx7X5gK1YZrOde4X_F3BTqrhyk-F8"

# Lyrics.ovh API URL for retrieving song lyrics
LYRICS_API_URL = 'https://api.lyrics.ovh/v1'

# Free Dictionary API URL for getting word meanings
DICTIONARY_API_URL = 'https://api.dictionaryapi.dev/api/v2/entries/en/'

# Define the SQLite database file path for storing word search history
DATABASE = './history.db'  # Change to the correct path if needed

def init_db():
    """Initialize the SQLite database with a table for storing words and their meanings."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    # Create a table for storing words along with the date, time, and meaning
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_time TEXT,
            word TEXT,
            meaning TEXT
        )
    """)
    conn.commit()  # Commit the changes to the database
    conn.close()  # Close the connection to the database

# Function to save a word and its meaning to the SQLite database
def save_word_to_history(word, meaning):
    """Saves the searched word and its meaning to the database."""
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Get current date and time
    conn = sqlite3.connect(DATABASE)  # Connect to the SQLite database
    cursor = conn.cursor()
    # Insert the word, meaning, and timestamp into the words table
    cursor.execute("INSERT INTO words (date_time, word, meaning) VALUES (?, ?, ?)", (date_time, word, meaning))
    conn.commit()  # Commit the changes to the database
    conn.close()  # Close the database connection

# Function to retrieve the history of saved words and meanings from the database
def get_history():
    """Retrieves all entries from the words history."""
    conn = sqlite3.connect(DATABASE)  # Connect to the SQLite database
    cursor = conn.cursor()
    # Select all words and their meanings, ordered by the most recent entries
    cursor.execute("SELECT date_time, word, meaning FROM words ORDER BY id DESC")
    history = cursor.fetchall()  # Fetch all rows from the query
    conn.close()  # Close the database connection
    return history  # Return the history

# Function to get an access token from the Spotify API using client credentials
def get_spotify_token():
    auth_url = "https://accounts.spotify.com/api/token"
    auth_data = {
        "grant_type": "client_credentials"  # Request token without user login (for public API access)
    }
    # Make a POST request to get the token, passing in client credentials
    auth_response = requests.post(auth_url, auth_data, auth=(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET))
    return auth_response.json().get('access_token')  # Extract the access token from the response

# Flask route for the home page
@app.route('/')
def index():
    return render_template('index.html')  # Render the main home page (index.html)

# Flask route for the 'Learn' page
@app.route('/learn')
def learn():
    return render_template('learn.html')  # Render the learning page (learn.html)

# Flask route for searching tracks on Spotify
@app.route('/search_spotify', methods=['POST'])
def search_spotify():
    query = request.form.get('query')  # Get the search query from the form
    token = get_spotify_token()  # Get the Spotify access token

    # Prepare the headers for the API request with the access token
    headers = {
        "Authorization": f"Bearer {token}"
    }
    # Make a search request to Spotify API for tracks matching the query
    search_url = f"https://api.spotify.com/v1/search?q={query}&type=track&limit=10"
    response = requests.get(search_url, headers=headers)
    data = response.json()  # Parse the response as JSON

    tracks = []
    # Check if the response contains tracks data
    if data.get('tracks'):
        for item in data['tracks']['items']:
            # Store the track name, artist, and Spotify URL in the results list
            tracks.append({
                'name': item['name'],
                'artist': item['artists'][0]['name'],
                'spotify_url': item['external_urls']['spotify'],
                'youtube_search_query': f"{item['name']} {item['artists'][0]['name']}"
            })
    return jsonify(tracks)  # Return the tracks as JSON

# Flask route for searching YouTube videos
@app.route('/search_youtube', methods=['POST'])
def search_youtube():
    query = request.form.get('query')  # Get the search query from the form
    # Make a search request to YouTube Data API for videos matching the query
    youtube_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&q={query}&key={YOUTUBE_API_KEY}&maxResults=1"
    response = requests.get(youtube_url)
    data = response.json()  # Parse the response as JSON

    video_url = None
    # Check if there are search results
    if data.get('items'):
        video_id = data['items'][0]['id']['videoId']  # Get the video ID of the first result
        video_url = f"https://www.youtube.com/watch?v={video_id}"  # Build the YouTube video URL
    return jsonify({'video_url': video_url})  # Return the video URL as JSON

# Flask route for retrieving song lyrics
@app.route('/get_lyrics', methods=['POST'])
def get_lyrics():
    artist = request.form.get('artist')  # Get the artist name from the form
    title = request.form.get('title')  # Get the song title from the form

    # Make a request to the Lyrics API for the specified artist and song title
    response = requests.get(f"{LYRICS_API_URL}/{artist}/{title}")
    if response.status_code == 200:  # Check if the request was successful
        data = response.json()
        lyrics = data.get('lyrics', 'Lyrics not found.')  # Get the lyrics from the response
    else:
        lyrics = 'Lyrics not found.'  # If the request failed, return 'Lyrics not found.'
    return jsonify({'lyrics': lyrics})  # Return the lyrics as JSON

# Flask route for retrieving word meanings
@app.route('/get_word_meaning', methods=['POST'])
def get_word_meaning():
    word = request.form.get('word')  # Get the word from the form
    # Make a request to the Free Dictionary API for the word's meaning
    response = requests.get(f"{DICTIONARY_API_URL}{word}")
    
    if response.status_code == 200:  # Check if the request was successful
        data = response.json()
        if data and isinstance(data, list) and 'meanings' in data[0]:
            # Get the first definition from the response
            definition = data[0]['meanings'][0]['definitions'][0]['definition']
            return jsonify({'meaning': definition})  # Return the meaning as JSON
    return jsonify({'meaning': 'No definition found'})  # Return a message if no definition was found

# Flask route for saving the searched word and meaning to the history
@app.route('/save_history', methods=['POST'])
def save_history():
    word = request.form.get('word')  # Get the word from the form
    meaning = request.form.get('meaning')  # Get the meaning from the form
    save_word_to_history(word, meaning)  # Save the word and meaning to the database
    return jsonify({'message': 'Word and meaning saved to history'})  # Return a success message

# Flask route for displaying the search history
@app.route('/get_history', methods=['GET'])
def see_history():
    history = get_history()  # Retrieve the word search history
    return render_template('history.html', history=history)  # Render the history page with the search history

# Main entry point of the application
if __name__ == '__main__':
    init_db()  # Initialize the database when the app starts
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)  # Run the Flask app on the specified host and port
