import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import csv

# Replace with your own client_id and client_secret
client_id = "6490107964544f35b78617b28d46ac0e"
client_secret = "fbea1b183bca4868a19d501b5fe9313b"

# Set up authentication
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=client_id,
                                                           client_secret=client_secret))

# Retrieve the playlist by ID
playlist_id = "37i9dQZF1DX4dyzvuaRJ0n"
playlist = sp.playlist(playlist_id)

# Print out information about the playlist
print(f"Name: {playlist['name']}")
print(f"Owner: {playlist['owner']['display_name']}")
print(f"Tracks: {playlist['tracks']['total']}")


def get_track_features(id):
    metadata = sp.track(id)
    features = sp.audio_features(id)

    # metadata
    name = metadata['name']
    album = metadata['album']['name']
    artists = [artist['name'] for artist in metadata['album']['artists']]
    artists_str = ', '.join(artists)
    release_date = metadata['album']['release_date']
    length = metadata['duration_ms']
    popularity = metadata['popularity']
    

    # audio features
    acousticness = features[0]['acousticness']
    danceability = features[0]['danceability']
    energy = features[0]['energy']
    instrumentalness = features[0]['instrumentalness']
    liveness = features[0]['liveness']
    loudness = features[0]['loudness']
    speechiness = features[0]['speechiness']
    tempo = features[0]['tempo']
    time_signature = features[0]['time_signature']

    track = [name, album, artists_str, release_date, length, popularity, danceability, acousticness, energy, instrumentalness, liveness, loudness, speechiness, tempo, time_signature]
    return track

# Get information about each track in the playlist
tracks = sp.playlist_tracks(playlist_id)["items"]
tracks_with_features = []
for track in tracks:
    track_id = str(track['track']['id'])
    tracks_with_features.append(get_track_features(track_id))

df = pd.DataFrame(tracks_with_features, columns = ['name', 
                                     'album', 
                                     'artists', 
                                     'release_date', 
                                     'length', 
                                     'popularity', 
                                     'danceability', 
                                     'acousticness', 
                                     'energy', 
                                     'instrumentalness', 
                                     'liveness', 
                                     'loudness', 
                                     'speechiness', 
                                     'tempo', 
                                     'time_signature'])

df.to_csv('playlist.csv', index=False)