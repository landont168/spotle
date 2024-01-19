"""
Spotle
Landon T.
Kitchener, Canada
"""

# Import libraries
import base64
import json
import os
import random
from datetime import datetime
from dotenv import load_dotenv
from requests import get, post
from titlecase import titlecase

# Declare constant
MAX_GUESSES = 5


class Artist:
    """Class representing an artist

    Attributes:
        name (str): The name of the artist
        artist_id (str): The unique Spotify ID of artist
        followers (int): The number of Spotify followers of artist
        related_artists (list): A list of other artists related to artist
        genres (list): A list of genres associated with the artist
        recent_album (date): The date of the release date of most recent album from artist
    """

    def __init__(self, name, artist_id, followers, related_artists, genres=None, recent_album=None):
        """Initialize instance of Artist class"""
        self.name = name
        self.artist_id = artist_id
        self.followers = followers
        self.related_artists = related_artists
        self.genres = genres
        self.recent_album = recent_album


    def __str__(self):
        """Return string representation of Artist object"""
        return (
            f"Artist("
            f"name={self.name}, "
            f"artist_id={self.artist_id}, "
            f"followers={self.followers}, "
            f"related_artists={self.related_artists}, "
            f"genres={self.genres}, "
            f"recent_album={self.recent_album})"
        )


    @classmethod
    def retrieve_artist_data(cls, token, name):
        """Retrieve artist data"""
        artist_name, artist_id, followers, genres = cls.get_artist_info(token, name)
        recent_album = cls.get_recent_album(token, artist_id)
        related_artists = cls.get_related_artists(token, artist_id)

        return cls(artist_name, artist_id, followers, related_artists, genres, recent_album)


    @staticmethod
    def get_artist_info(token, name):
        """Get artist name, ID, followers, genres for artist"""
        # Set up query
        url = f"https://api.spotify.com/v1/search?q={name}&type=artist&limit=1"
        headers = get_auth_header(token)

        # Get JSON result
        result = get(url, headers=headers)
        json_result = json.loads(result.content)["artists"]["items"]

        # Artist does not exist
        if len(json_result) == 0:
            print("Artist name does not exist")
            return None

        # Return artist information
        artist_result = json_result[0]
        artist_name = artist_result["name"]
        artist_id = artist_result["id"]
        followers = artist_result["followers"]["total"]
        genres = artist_result["genres"]
        return artist_name, artist_id, followers, genres

    @staticmethod
    def get_recent_album(token, artist_id):
        """Get release date of most recent album"""
        # Set up query
        url = f"https://api.spotify.com/v1/artists/{artist_id}/albums?include_groups=album&country=US"
        headers = get_auth_header(token)

        # Get JSON result
        result = get(url, headers=headers)
        album_result = json.loads(result.content)["items"]

        # Return release date of most recent album
        if len(album_result) == 0:
            return None
        recent_album = datetime.strptime(album_result[0]["release_date"], "%Y-%m-%d")
        return recent_album

    @staticmethod
    def get_related_artists(token, artist_id):
        """Get list of related artists"""
        url = f"https://api.spotify.com/v1/artists/{artist_id}/related-artists?"
        headers = get_auth_header(token)

        # Get JSON result
        result = get(url, headers=headers)
        artists = json.loads(result.content)["artists"][:5]

        # Get top five most related artists
        related_artists = []
        for artist in artists:
            related_artist = artist["name"]
            related_artists.append(related_artist)
        return related_artists


def get_token():
    """Load client ID and secret to obtain access token for Spotify API"""

    # Load client ID and secret
    load_dotenv()
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")

    # Encode concatenated string
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    # Send authorization request to obtain token
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}

    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token


def get_auth_header(token):
    """Construct header for web API calls"""
    return {"Authorization": "Bearer " + token}


def get_top_artists(token):
    """Get list of artists from featured playlist"""

    # Set up query
    url = "https://api.spotify.com/v1/browse/featured-playlists?country=US"
    headers = get_auth_header(token)

    # Get certain playlist
    result = get(url, headers=headers)
    playlists = json.loads(result.content)["playlists"]["items"]
    playlist = get_playlist(playlists)

    # Get tracks of playlist
    tracks_url = playlist["tracks"]["href"]
    tracks_result = get(tracks_url, headers=headers)
    tracks = json.loads(tracks_result.content)["items"]

    # Get unique artists from tracks
    top_artists = set()
    for track in tracks:
        artists = track["track"]["artists"]
        for artist in artists:
            artist_name = artist["name"]
            top_artists.add(artist_name)
    return list(top_artists)


def get_playlist(playlists):
    """Get specific playlist from JSON of playlists"""
    for playlist in playlists:
        if playlist["name"] == "Viral Hits":
            return playlist


def get_mystery_artist(artists):
    """Randomly choose mystery artist from list"""
    return random.choice(artists)


def check_followers(g_artist, m_artist):
    """Compares follower count between artists"""
    g_artist_followers = g_artist.followers
    m_artist_followers = m_artist.followers

    if g_artist_followers > m_artist_followers:
        return "🔽 LESS FOLLOWERS"
    elif m_artist_followers > g_artist_followers:
        return "🔼 MORE FOLLOWERS"
    else:
        return "🟰 SAME NUMBER OF FOLLOWERS"


def check_genres(g_artist, m_artist):
    """Extracts common genres between artists"""
    g_artist_genres = g_artist.genres
    m_artist_genres = m_artist.genres
    common_genres = set(g_artist_genres) & set(m_artist_genres)

    if len(common_genres) == 0:
        return "🥀 NO COMMON GENRES"
    else:
        return f"🎶 COMMON GENRES: {titlecase(', '.join(sorted(common_genres)))}"


def check_recent_album(g_artist, m_artist):
    """Compares release dates of most recent album between artists"""
    g_artist_recent_album = g_artist.recent_album
    m_artist_recent_album = m_artist.recent_album

    if not g_artist_recent_album:
        return "👽 YOUR GUESS HAS NOT RELEASED AN ALBUM..."
    elif not m_artist_recent_album:
        return "❓ MYSTERY ARTIST HAS NOT RELEASED AN ALBUM..."
    elif g_artist_recent_album > m_artist_recent_album:
        return "⌛ LESS RECENT ALBUM RELEASE"
    elif m_artist_recent_album > g_artist_recent_album:
        return "⏳ MORE RECENT ALBUM RELEASE"
    else:
        return "⏰ SAME RECENT ALBUM RELEASE"


def check_related_artists(g_artist, m_artist):
    """Determine if artist guess is related artist to mystery artist"""
    g_artist_name = g_artist.name
    m_artist_related = m_artist.related_artists

    if g_artist_name in m_artist_related:
        return "🐈 SIMILAR ARTIST"
    else:
        return "🐕 DISSIMILAR ARTIST"


def engine(token, mystery_artist):
    """Run game for player"""

    guesses = 0
    previous_guesses = []

    while guesses < MAX_GUESSES:
        guess_artist_name = input(f"Guess #{guesses+1}: ")
        guess_artist = Artist.retrieve_artist_data(token, guess_artist_name)

        # Artist already guessed
        guess_artist_id = guess_artist.artist_id
        if guess_artist_id in previous_guesses:
            print("🤡 ALREADY GUESSED. TRY AGAIN!")

        # Congratulate correct guess
        elif guess_artist.artist_id == mystery_artist.artist_id:
            print(f"🎉 CONGRATULATIONS! THE MYSTERY ARTIST WAS: {mystery_artist.name.upper()}!")
            return None

        # Provide feedback for incorrect guess
        else:
            feedback(guess_artist, mystery_artist)
            previous_guesses.append(guess_artist_id)
            guesses += 1

    # Reveal mystery artist upon failure
    game_over(mystery_artist)


def feedback(guess_artist, mystery_artist):
    """Provide feedback to player"""
    print(check_followers(guess_artist, mystery_artist))
    print(check_genres(guess_artist, mystery_artist))
    print(check_recent_album(guess_artist, mystery_artist))
    print(check_related_artists(guess_artist, mystery_artist))
    print()


def welcome():
    """Welcoming print statements"""
    print()
    print("Welcome to Spotle 🎹! The aim is to guess a musical artist.")
    print("If you guess wrong, we will give you a few cheeky hints. Have fun! 🕵️")
    print()


def game_over(mystery_artist):
    """Reveal mystery artist upon failure"""
    print("😺 NICE TRY, BETTER LUCK NEXT TIME!")
    print(f"THE MYSTERY ARTIST WAS: {mystery_artist.name.upper()} 🙈")
    print()


def main():
    """Set up and run game"""
    token = get_token()
    top_artists = get_top_artists(token)
    mystery_artist = Artist.retrieve_artist_data(token, get_mystery_artist(top_artists))
    welcome()
    engine(token, mystery_artist)


if __name__ == "__main__":
    main()
