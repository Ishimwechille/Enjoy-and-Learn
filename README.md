# Enjoy and Learn 🎶📚

Enjoy and Learn is a web application designed to enhance the music-listening experience by integrating song search, playback, lyrics, and word definitions. Users can search for songs from Spotify, play them on YouTube, view the lyrics, and get dictionary definitions by clicking on any word. Feedback from users is automatically sent to our email, and their search and playback history are stored.

## Features

- **Song Search**: Search for songs using Spotify’s API.
- **Playback on YouTube**: Play searched songs directly via YouTube integration.
- **Lyrics Display**: Fetch and display lyrics of the chosen song.
- **Word Definition**: Click on any word in the lyrics to get its dictionary meaning.
- **History Tracking**: Stores user search and playback history.
- **User Feedback**: Users can submit feedback, which is emailed directly to us.
  
## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite3 (for storing search and playback history)
- **Hosting**: Render (free tier)
- **APIs**:
  - **Spotify API**: For song search
  - **YouTube API**: For song playback
  - **Lyrics API**: For lyrics retrieval
  - **Dictionary API**: For word definitions

## Project Structure

```plaintext
├── app.py                # Main Flask application
├── templates/
│   ├── index.html        # Landing page
│   ├── learn.html        # Main app interface
│   └── navbar.html       # Navigation bar component
├── static/
│   ├── css/
│   │   └── styles.css    # Custom CSS styles
│   ├── js/
│   │   └── scripts.js    # JavaScript functionality
├── requirements.txt      # Dependencies
├── README.md             # Project README
└── .env                  # API keys and sensitive config (not included)
