import os
from flask import Flask, render_template, request, redirect

import spotipy 
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

import requests
import numpy as np
import json
import functools

app = Flask(__name__)
access_token = 'BQATbWjqAFVXPSAJyi8YgMnEW2BMnV8NAr2lT4Pch6crmN27QfDodocwHsxyRQ-6TyYok2EDNh5W55C4UNde9mUDI5ZuH-i_s1-ateqyuzWZ2kRXUlXAcTTDNxAv_OJ-u3EWKWilSdu-PsNyClSjp1e0VWGwx_ojJUflrBGaiQuGZTPpW1CiGLDrgu4XpP3YktbcR6_hz1BwaamV6YHvchDo-qDIPDkcVnLtzNliKMbwSPHmXDMsj2E7_pbAdCUgNFx_-uyBBPNtyd4j0jEHh-M6mKbizKKtpWrz'
head = {'Authorization': 'Bearer {}'.format(access_token)}

spotify = spotipy.Spotify()

SPOTIPY_CLIENT_ID=''
SPOTIPY_CLIENT_SECRET=''
SPOTIPY_REDIRECT_URI='http://127.0.0.1:5000/callback'

scc = SpotifyClientCredentials(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET)

@app.route('/', methods=['GET','POST'])
def index():
	if request.method == 'POST':
		message = request.form['message']
		return redirect("/"+message)
	return render_template('index.html')

@functools.lru_cache()
def find_track(name):
	"""token = util.prompt_for_user_token("catherinecang",'user-library-read',client_id='ab850d0e231e4fe69a0ee40e95792610',
														client_secret='c372bfb8f8a54e529c3255f5c4211664',redirect_uri='http://127.0.0.1:5000/callback')
				if token:
					spotify = spotipy.Spotify(auth=token)"""
	sp = spotipy.Spotify(client_credentials_manager=scc)
	res = sp.search(q=name, type="track", limit=50)
	for r in res['tracks']['items']:
		if r['name'].lower() == name.lower():
			return r
"""	url = 'https://api.spotify.com/v1/search?q={}&type=track&limit=50'.format(name)
	response = requests.get(url, headers=head).json()
	for r in response['tracks']['items']:
		if r['name'].lower() == name.lower():
			return r
	for k in range(3):
		url = 'https://api.spotify.com/v1/search?q={}&type=track&offset={}&limit=50'.format(name, 50*(k+1))
		response = requests.get(url, headers=head).json()
		for r in response['tracks']['items']:
			if r['name'].lower() == name.lower():
				return r"""

def get_tracks(full_str):
	full_str = full_str.lower()
	str_split = full_str.split()
	track_lst = []
	if not full_str:
		return []
	elif len(str_split) == 1:
		return [find_track(full_str)]
	while str_split:
		curr_str = str_split[0]
		saved = curr_str
		print("aaa", str_split, saved)

		for i in range(1, min(3, len(str_split))):
			curr_str += ' ' + str_split[i]
			print(curr_str, i)
			if find_track(curr_str):
				saved = curr_str
		print("here: " + saved)
		if not find_track(saved):
			print(saved)
			return None

		track_lst += [find_track(saved)]
		str_split = str_split[len(saved.split()):]
		print(str_split)
	return track_lst

@app.route("/<message>")
def get_tracks_r(full_str):
	full_str = full_str.lower()
	str_split = full_str.split()
	track_lst = []
	if not full_str:
		return []
	elif len(str_split) == 1:
		return [[find_track(full_str)]]
	for i in range(1, min(4, len(str_split)+1)):
		first = find_track(list_to_str(str_split[:i]))
		if first:
			if i == len(str_split):
				track_lst.append([first])
			else:
				rest = get_tracks_r(list_to_str(str_split[i:]))
				if rest:
					track_lst += [[first] + r for r in rest]
	return track_lst

def list_to_str(lst):
	return ' '.join(lst)


def save_common_words():
	common_lst = {}
	url = 'https://api.spotify.com/v1/tracks/5cIZoKmBiFgjabaBG0D9fO'
	response = requests.get(url, headers=head).json()
	common_lst['and'] = response
	with open('common.json', 'w') as fp:
		json.dump(common_lst, fp)

def load_common_words():
	with open('common.json', 'r') as fp:
   		return json.load(fp)


