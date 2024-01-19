"""
Spotle
Landon T.
Kitchener, Canada
"""

from project import (
    get_token,
    Artist,
    check_followers,
    check_genres,
    check_recent_album,
    check_related_artists,
)


# Get token
token = get_token()


# Configure artist objects
drake = Artist.retrieve_artist_data(token, "Drake")
future = Artist.retrieve_artist_data(token, "Future")
travis_scott = Artist.retrieve_artist_data(token, "Travis Scott")
taylor_swift = Artist.retrieve_artist_data(token, "Taylor Swift")


def test_check_followers():
    assert check_followers(travis_scott, drake) == "🔼 MORE FOLLOWERS"
    assert check_followers(drake, travis_scott) == "🔽 LESS FOLLOWERS"
    assert check_followers(drake, future) == "🔽 LESS FOLLOWERS"
    assert check_followers(future, drake) == "🔼 MORE FOLLOWERS"
    assert check_followers(future, travis_scott) == "🔼 MORE FOLLOWERS"
    assert check_followers(travis_scott, future) == "🔽 LESS FOLLOWERS"


def test_check_genres():
    assert check_genres(travis_scott, drake) == "🎶 COMMON GENRES: Hip Hop, Rap"
    assert check_genres(travis_scott, future) == "🎶 COMMON GENRES: Hip Hop, Rap"
    assert check_genres(taylor_swift, drake) == "🥀 NO COMMON GENRES"
    assert check_genres(taylor_swift, future) == "🥀 NO COMMON GENRES"
    assert check_genres(taylor_swift, travis_scott) == "🥀 NO COMMON GENRES"


def test_check_recent_album():
    assert check_recent_album(travis_scott, drake) == "⏳ MORE RECENT ALBUM RELEASE"
    assert check_recent_album(drake, travis_scott) == "⌛ LESS RECENT ALBUM RELEASE"
    assert check_recent_album(drake, future) == "⌛ LESS RECENT ALBUM RELEASE"
    assert check_recent_album(future, drake) == "⏳ MORE RECENT ALBUM RELEASE"
    assert check_recent_album(future, travis_scott) == "⏳ MORE RECENT ALBUM RELEASE"
    assert check_recent_album(travis_scott, future) == "⌛ LESS RECENT ALBUM RELEASE"


def test_check_related_artists():
    assert check_related_artists(future, drake) == "🐈 SIMILAR ARTIST"
    assert check_related_artists(travis_scott, drake) == "🐈 SIMILAR ARTIST"
    assert check_related_artists(future, travis_scott) == "🐈 SIMILAR ARTIST"
    assert check_related_artists(taylor_swift, drake) == "🐕 DISSIMILAR ARTIST"
    assert check_related_artists(taylor_swift, travis_scott) == "🐕 DISSIMILAR ARTIST"
    assert check_related_artists(taylor_swift, future) == "🐕 DISSIMILAR ARTIST"
