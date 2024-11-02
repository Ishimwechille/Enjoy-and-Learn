from flask import Flask, render_template, request, jsonify
import requests
import sqlite3
from datetime import datetime
import os
from flask_mail import Mail, Message  # Import Flask-Mail

app = Flask(__name__)

# Flask-Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'ishimweachille2@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'zytk xlyp tpqh iapc'  # Replace with your email password
app.config['MAIL_DEFAULT_SENDER'] = 'achilleishimwe886@gmail.com'  # Replace with your email

mail = Mail(app)  # Initialize Mail

# Spotify API Credentials
SPOTIFY_CLIENT_ID = 'bc93a10a093245ceb6d8610f0825ee86'
SPOTIFY_CLIENT_SECRET = '6f25a2ad278c4d04bb9b1f109be7f03d'

# YouTube API Key
YOUTUBE_API_KEY = "AIzaSyAr14gx7X5gK1YZrOde4X_F3BTqrhyk-F8"

# Lyrics.ovh for Lyrics API
LYRICS_API_URL = 'https://api.lyrics.ovh/v1'

# Free Dictionary API for word meanings
DICTIONARY_API_URL = 'https://api.dictionaryapi.dev/api/v2/entries/en/'

# SQLite database setup
DATABASE = './history.db'  # Update with your database path

def init_db():
    """Initialize the SQLite database with the words and feedback tables if they don't exist."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Create words table
    cursor.execute("""CREATE TABLE IF NOT EXISTS words (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date_time TEXT,
        word TEXT,
        meaning TEXT
    )""")
    
    # Create feedback table
    cursor.execute("""CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date_time TEXT,
        name TEXT,
        email TEXT,
        message TEXT
    )""")
    
    conn.commit()
    conn.close()

# Function to save a word and its meaning to history
def save_word_to_history(word, meaning):
    """Saves the searched word and its meaning to the database."""
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO words (date_time, word, meaning) VALUES (?, ?, ?)", (date_time, word, meaning))
    conn.commit()
    conn.close()

# Function to retrieve word history
def get_history():
    """Retrieves all entries from the words history."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT date_time, word, meaning FROM words ORDER BY id DESC")
    history = cursor.fetchall()
    conn.close()
    return history

# Function to get Spotify token
def get_spotify_token():
    auth_url = "https://accounts.spotify.com/api/token"
    auth_data = {
        "grant_type": "client_credentials"
    }
    auth_response = requests.post(auth_url, auth_data, auth=(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET))
    return auth_response.json().get('access_token')

@app.route('/')
def index():
    return render_template('index.html')  # Render index.html for the home page

@app.route('/learn')
def learn():
    return render_template('learn.html')  # Render learn.html for the learn page

@app.route('/search_spotify', methods=['POST'])
def search_spotify():
    query = request.form.get('query')
    token = get_spotify_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }
    search_url = f"https://api.spotify.com/v1/search?q={query}&type=track&limit=10"
    response = requests.get(search_url, headers=headers)
    data = response.json()

    tracks = []
    if data.get('tracks'):
        for item in data['tracks']['items']:
            tracks.append({
                'name': item['name'],
                'artist': item['artists'][0]['name'],
                'spotify_url': item['external_urls']['spotify'],
                'youtube_search_query': f"{item['name']} {item['artists'][0]['name']}"
            })
    return jsonify(tracks)

@app.route('/search_youtube', methods=['POST'])
def search_youtube():
    query = request.form.get('query')
    youtube_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&q={query}&key={YOUTUBE_API_KEY}&maxResults=1"
    response = requests.get(youtube_url)
    data = response.json()

    video_url = None
    if data.get('items'):
        video_id = data['items'][0]['id']['videoId']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
    return jsonify({'video_url': video_url})

@app.route('/get_lyrics', methods=['POST'])
def get_lyrics():
    artist = request.form.get('artist')
    title = request.form.get('title')

    response = requests.get(f"{LYRICS_API_URL}/{artist}/{title}")
    if response.status_code == 200:
        data = response.json()
        lyrics = data.get('lyrics', 'Lyrics not found.')
    else:
        lyrics = 'Lyrics not found.'
    return jsonify({'lyrics': lyrics})

@app.route('/get_word_meaning', methods=['POST'])
def get_word_meaning():
    word = request.form.get('word')
    response = requests.get(f"{DICTIONARY_API_URL}{word}")
    
    if response.status_code == 200:
        data = response.json()
        if data and isinstance(data, list) and 'meanings' in data[0]:
            definition = data[0]['meanings'][0]['definitions'][0]['definition']
            return jsonify({'meaning': definition})
    return jsonify({'meaning': 'No definition found'})

@app.route('/save_history', methods=['POST'])
def save_history():
    word = request.form.get('word')
    meaning = request.form.get('meaning')
    save_word_to_history(word, meaning)
    return jsonify({'message': 'Word and meaning saved to history'})

@app.route('/get_history', methods=['GET'])
def see_history():
    history = get_history()
    return render_template('history.html', history=history)

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO feedback (date_time, name, email, message) VALUES (?, ?, ?, ?)", 
                   (date_time, name, email, message))
    conn.commit()
    conn.close()
    
    # Send email with feedback details
    msg = Message("New Feedback Received",
                  recipients=['niyokwizerajd123@gmail.com'])  # Your email
    msg.body = f"Name: {name}\nEmail: {email}\nMessage: {message}\nDate & Time: {date_time}"
    mail.send(msg)  # Send email to given receiver
    
    return jsonify({'message': 'Feedback submitted successfully!'})

@app.route('/get_feedback', methods=['GET'])
def get_feedback():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT date_time, name, email, message FROM feedback ORDER BY id DESC")
    feedbacks = cursor.fetchall()
    conn.close()
    return render_template('feedback.html', feedbacks=feedbacks)

if __name__ == '__main__':
    init_db()  # Initialize the database when the app starts
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
