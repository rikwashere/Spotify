from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
from getkeys import getkeys
import unicodecsv as csv
import requests
import spotipy
import json
import time
import sys

def getURI(url):

	uri = 'spotify:' + ':'.join(url.split('/')[-4:])
	return uri

keys = getkeys()

SPOTIPY_CLIENT_ID=keys['SPOTIPY_CLIENT_ID']
SPOTIPY_CLIENT_SECRET=keys['SPOTIPY_CLIENT_SECRET']
SPOTIPY_REDIRECT_URI=keys['SPOTIPY_REDIRECT_URI']

auth = spotipy.oauth2.SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, proxies=None)

sp = spotipy.Spotify(auth=auth.get_access_token())

if len(sys.argv) > 1: 
	url = sys.argv[1]
else:
	sys.exit('Please supply URL to playlist')

uri = getURI(url)

print uri

username = uri.split(':')[2]
playlist_id = uri.split(':')[4]

response = sp.user_playlist(username, playlist_id)

name = response['name']

results = []

response = response['tracks']


while response['next']:
	tracks = response['items']
	for track in tracks:
		track = track['track']
		track_str = track['name']
		artists_str = ', '.join([artist['name'] for artist in track['artists']])
		print '%s by %s, %s' % (track_str, artists_str, track['id'])

		features = sp.audio_features(str(track['id']))[0]
		keys = ['energy', 'liveness', 'tempo', 'speechiness', 'acousticness', 'instrumentalness', 'danceability', 'key', 'duration_ms', 'loudness', 'valence']
		data = [features[key] for key in keys]

		out = [track['id'], track_str, artists_str]
		out += data
		results.append(out)
		#time.sleep(1)
	response = sp.next(response)
else:
	tracks = response['items']
	for track in tracks:
		track = track['track']
		track_str = track['name']
		artists_str = ', '.join([artist['name'] for artist in track['artists']])
		print '%s by %s, %s' % (track_str, artists_str, track['id'])

		features = sp.audio_features(str(track['id']))[0]
		keys = ['energy', 'liveness', 'tempo', 'speechiness', 'acousticness', 'instrumentalness', 'danceability', 'key', 'duration_ms', 'loudness', 'valence']
		data = [features[key] for key in keys]

		out = [track['id'], track_str, artists_str]
		out += data
		results.append(out)

keys = ['energy', 'liveness', 'tempo', 'speechiness', 'acousticness', 'instrumentalness', 'danceability', 'key', 'duration_ms', 'loudness', 'valence']


with open(name + '.tab', 'w') as csv_out:
	writer = csv.writer(csv_out, delimiter='\t')
	writer.writerow(['id', 'title', 'artists'] + keys)
	writer.writerows(results)
