import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import lyricsgenius
import pandas as pd

def get_playlist_tracks(playlist_id):
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

def get_lyrics(song_name, artist):
    song = genius.search_song(song_name, artist)

    if song:
        return song.lyrics
    else:
        return "Lyrics not found."

# Your Spotify API credentials
client_id = '56a9549d52ac457ca9d3e7854d62c33c'
client_secret = '1360e3875f6e4fe29289a2053c9b241a'

genius = lyricsgenius.Genius("i9B19P8ni0wHxiya15JepeExxqj9mx5ldse83a6s4grpZlvgXwzbKDid9V8qW7vD")
# Initialize Spotipy
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Spotify ID of the "Today's Top Hits" playlist (replace with your target playlist ID)
playlist_id = '37i9dQZF1DX32NsLKyzScr'

tracks = get_playlist_tracks(playlist_id)

# Print the names of the tracks
final_data = []
for track in tracks:  # Just showing the first 10 tracks as an example
    track_name = track['track']['name']
    artist_name = track['track']['artists'][0]['name']  # Name of the first artist
    track_lyric = get_lyrics(track_name, artist_name)
    print(f"{track_name} by {artist_name}")
    final_data.append({'Song Name' : track_name, 'Artist' : artist_name, 'Lyrics' : track_lyric})


df = pd.DataFrame(final_data)

excel_file_path = 'ofek.xlsx'
df.to_excel(excel_file_path, index=False)

print(f"Excel file '{excel_file_path}' created successfully with {len(final_data)} songs.")

