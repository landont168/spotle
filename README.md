# 🎙️ Spotle
#### Video Demo 📹:  https://www.youtube.com/watch?v=y0sgZvjW59Q
#### Description 👁️‍🗨️: An artist-themed Wordle game built with Python using the Spotify Web API.


##### Game 🕹️:
The aim of the game for the player is to guess the "mystery artist" within five attempts. If a player guesses the correct artist, the game simply ends. Otherwise, the game will provide some hints for the player based on their artist guess. Specifically, feedback is provided based on a comparison between the player's artist guess and the actual mystery artist. Let's use an example to better understand the game. Suppose famous Canadian rapper Drake was the mystery artist and the player guessed Travis Scott as their very first guess. Then, the game will provide hints related to the artist's:
1. Number of Spotify followers
2. Associated genres
3. Release of their most recent album
4. Related artists

In this case, as of December 2023, we have that:
1. Drake has more followers than Travis Scott
2. Drake and Travis Scott are both associated with the Hip Hop and Rap genres
3. Drake has released a more recent album (For All the Dogs - Oct 6, 2023) compared to Travis Scott's less recent album (UTOPIA - July 28, 2023)
4. Drake and Travis Scott are considered similar artists, based on analysis of the Spotify community's listening history

Hence, the game will correspondingly output the following to indicate all of this information:

```
🔼 MORE FOLLOWERS

🎶 COMMON GENRES: Hip Hop, Rap

⏳ MORE RECENT ALBUM RELEASE

🐈 SIMILAR ARTIST

The player may continue guessing until they correctly guess the artist or run out of guesses!
```

---

##### Functionality 🧰:

In the main file ```project.py```, it contains simple Python scripts and functions that use the Spotify Web API to accomplish 4 main components:
1. Request an access token in order to make Spotify Web API calls
- Uses ```dotenv``` module to load in the ```CLIENT_ID``` and ```CLIENT_SECRET```
- Sends a POST request to the ```/api/token``` endpoint of the Spotify OAuth 2.0 Service to retrieve the access ```token``` as part of JSON data
- Creates required ```headers``` for GET requests

2. Retrieve a list of top artists from a unique featured playlist from Spotify
- Retrieves all the ```tracks``` from the "Viral Hits" featured Spotify playlist
- Retrieves the ```top_artists``` from the list of tracks

3. Retrieve the necessary information about an artist
- Creates ```Artist``` object for a particular artist based on their name
- Uses Spotify Web API to gather the necessary information of the artist (ex. Spotify ID, Spotify followers, associated genres, release date of their most recent album, and related artists)

4. Simulate the game and providing feedback to the player if needed
- Pick a random artist from the list of top artists to be the ```mystery_artist```
- Repeatedly prompts player for guess until they correctly guess the mystery artist or reach the maximum number of allowed guesses
- Provides feedback according to the player's guess and information regarding the mystery artist

---

##### Design 🎨:

A design choice that I debated was whether I needed to store the information for an artist in a dictionary or class. In the end, I decided to create an ```Artist``` object for a particular artist as it felt more intuitive to store the attributes within a class rather than keys and values in a plain dictionary. It also allowed me to modularize the ```retrieve_artist_data```, ```get_artist_info```, ```get_recent_album```, and ```get_related_artists``` functions within the ```Artist``` class, improving the design of the code.

---

#### Next Steps ⏭️:

To further enhance this project, I plan to build a proper web application, similar to Wordle, that will allow users to interactively play the game. I want to be able to include images, store the data better using SQL, eliminating the need to constantly use to Spotify Web API to gather artist information. Furthermore, I plan to use Python and Flask, along with HTML, CSS, and Bootstrap to help me configure and design the web application.
