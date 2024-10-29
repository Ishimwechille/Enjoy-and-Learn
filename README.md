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
│   └── navbar.html
    └── feedback.html       # Navigation bar component
├── static/
│   ├── css/
│   │   └── styles.css    # Custom CSS styles
│   ├── js/
│   │   └── scripts.js    # JavaScript functionality
├── requirements.txt      # Dependencies
├── README.md             # Project README
└── .env                  # API keys and sensitive config (not included)

Setup Instructions
Clone the repository:

bash
Copy code
git clone https://github.com/your-username/enjoy-and-learn.git
cd enjoy-and-learn
Install dependencies: Make sure you have Python installed, then run:

bash
Copy code
pip install -r requirements.txt
Set up environment variables: Create a .env file with the following API keys (you may need to register for some):

makefile
Copy code
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
YOUTUBE_API_KEY=your_youtube_api_key
LYRICS_API_KEY=your_lyrics_api_key
DICTIONARY_API_KEY=your_dictionary_api_key
EMAIL=your_email_address
EMAIL_PASSWORD=your_email_password
Initialize the database:

bash
Copy code
flask shell
>>> from app import db
>>> db.create_all()
Run the application:

bash
Copy code
flask run
The application will be accessible at http://127.0.0.1:5000.

Usage
Search for Songs: Use the search bar to find songs from Spotify.
Play Songs on YouTube: Click on the desired song to play it via YouTube.
Get Lyrics: View song lyrics, which are displayed automatically after selecting a song.
Word Meaning: Click on any word in the lyrics to get its definition from the dictionary.
Submit Feedback: Use the feedback form to submit your thoughts, which we will receive via email.
View History: Your search and playback history is stored and accessible for easy navigation.
Hosting and Deployment
This project is hosted on Render, a free hosting service for web applications.

Create a new Flask project on Render.
Connect your GitHub repository to Render.
Add environment variables in Render's dashboard as configured in the .env file.
Deploy your application.
Contributing
Contributions are welcome! Please submit a pull request if you have a feature or fix in mind.

License
This project is licensed under the MIT License - see the LICENSE file for details.
