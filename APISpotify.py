import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import lyricsgenius
import pandas as pd

# Spotify Authentication
spotify = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id="Add_ClientID",
        client_secret="Add-SecretID",
    )
)

# Genius Authentication
genius = lyricsgenius.Genius(
    "i9B19P8ni0wHxiya15JepeExxqj9mx5ldse83a6s4grpZlvgXwzbKDid9V8qW7vD"
)


def fetch_songs_from_spotify():
    songs = []
    playlist_ids = [
        "37i9dQZEVXbMDoHDwVN2tF",
        "37i9dQZF1DXcBWIGoYBM5M",
        "37i9dQZF1DX0XUsuxWHRQd",
        "37i9dQZF1DWXRqgorJj26U",
        "37i9dQZF1DX4dyzvuaRJ0n",
        "37i9dQZF1DX1lVhptIYRda",
        "37i9dQZF1DX10zKzsJ2jva",
        "37i9dQZF1DX4sWSpwq3LiO",
        "37i9dQZF1DX5uokaTN4FTR",
        "37i9dQZF1DXbITWG1ZJKYt",
        "37i9dQZF1DWWEJlAGA9gs0",
    ]

    for playlist_id in playlist_ids:
        offset = 0
        while True:
            # Example: Fetch tracks from the 'Global Top 50' playlist
            tracks = spotify.playlist_tracks(
                "spotify:playlist:{}".format(playlist_id), offset=offset
            )["items"]
            if len(tracks) == 0:
                break

            for track in tracks:
                track_data = track["track"]
                songs.append(
                    {
                        "name": track_data["name"],
                        "album_type": track_data["album"]["album_type"],
                        "artist": track_data["artists"][0][
                            "name"
                        ],  # Taking the first artist
                        "album": track_data["album"]["name"],
                        "year": track_data["album"]["release_date"][
                            :4
                        ],  # Extracting year from release_date
                        "length": track_data["duration_ms"],
                        "spotify_id": track_data[
                            "id"
                        ],  # We'll use this to avoid duplicates
                        "popularity": track_data["popularity"],
                        "playlist_id": playlist_id,
                    }
                )

            offset += len(tracks)
        print("Spotify fetched {} songs".format(offset))

    return songs


def add_lyrics_from_genius(songs):
    index = 1
    for song in songs:
        try:
            genius_song = genius.search_song(song["name"], song["artist"])
            song["lyrics"] = (
                genius_song.lyrics[genius_song.lyrics.find("Lyrics") + 6 :]
                if genius_song
                else "Lyrics not found"
            )
            # song['views'] = genius_song.stats['pageviews'] if genius_song and 'pageviews' in genius_song.stats else "Views not available"
        except Exception as e:
            print(f"Error fetching lyrics for {song['name']} by {song['artist']}: {e}")
            song["lyrics"] = "Lyrics not found"
            # song['views'] = "Views not available"

        print("Genius for song: {}".format(index))
        index += 1


def save_songs_to_excel(songs, filename="WordSongsData.xlsx"):
    df = pd.DataFrame(songs)
    df.to_excel(filename, index=False)


# Fetch songs from Spotify
songs = fetch_songs_from_spotify()
print("Total songs count is {}".format(len(songs)))
# Add lyrics and views from Genius
add_lyrics_from_genius(songs)

# Save to Excel
save_songs_to_excel(songs)
