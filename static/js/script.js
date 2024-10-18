document.getElementById('search-button').onclick = function() {
    const query = document.getElementById('song-query').value;
    fetch('/search_spotify', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: `query=${encodeURIComponent(query)}`
    })
    .then(response => response.json())
    .then(data => {
        const resultsList = document.getElementById('spotify-results');
        resultsList.innerHTML = '';
        data.forEach(track => {
            const li = document.createElement('li');
            li.innerHTML = `${track.name} by ${track.artist} 
                            <button onclick="playSong('${track.artist}', '${track.name}', '${track.youtube_search_query}')">Play</button>`;
            resultsList.appendChild(li);
        });
    });
};

function playSong(artist, title, query) {
    const resultsList = document.getElementById('spotify-results');
    resultsList.innerHTML = `<li>${title} by ${artist} <button onclick="playSong('${artist}', '${title}', '${query}')">Play</button></li>`;
    playOnYouTube(query);
    getLyrics(artist, title);
}

function playOnYouTube(query) {
    fetch('/search_youtube', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: `query=${encodeURIComponent(query)}`
    })
    .then(response => response.json())
    .then(data => {
        const youtubeVideoDiv = document.getElementById('youtube-video');
        youtubeVideoDiv.innerHTML = '';
        if (data.video_url) {
            const iframe = document.createElement('iframe');
            iframe.src = data.video_url.replace('watch?v=', 'embed/');
            iframe.frameBorder = "0";
            iframe.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture";
            iframe.allowFullscreen = true;
            youtubeVideoDiv.appendChild(iframe);
        }
    });
}

function getLyrics(artist, title) {
    fetch('/get_lyrics', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: `artist=${encodeURIComponent(artist)}&title=${encodeURIComponent(title)}`
    })
    .then(response => response.json())
    .then(data => {
        displayLyrics(data.lyrics);
    });
}

function displayLyrics(lyricsText) {
    const lyricsContainer = document.getElementById('lyrics');
    lyricsContainer.innerHTML = '';
    const words = lyricsText.split(' ');
    words.forEach(word => {
        const wordElement = document.createElement('span');
        wordElement.innerText = word + ' ';
        wordElement.style.cursor = 'pointer';
        wordElement.onclick = function() {
            fetchWordMeaning(word);
        };
        lyricsContainer.appendChild(wordElement);
    });
}

function fetchWordMeaning(word) {
    fetch('/get_word_meaning', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: `word=${encodeURIComponent(word)}`
    })
    .then(response => response.json())
    .then(data => {
        const meaning = data.meaning || 'No definition found';
        document.getElementById('word-meaning').innerText = `Meaning of "${word}": ${meaning}`;
    });
}
