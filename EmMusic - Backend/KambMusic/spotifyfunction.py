import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import glob
#import pandas as pd
import json
import webbrowser
from spotipy.oauth2 import SpotifyOAuth
import requests
import random
import os
from django.http import JsonResponse, HttpResponse

def getTrackURL(emotion):
    SPOTIPY_CLIENT_ID='<your-client-id>'
    SPOTIPY_CLIENT_SECRET='<your-client-secret>'
    SPOTIPY_REDIRECT_URI='<redirect-url'
    USERNAME = '<your-username>'
    client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    AUTH_URL = 'https://accounts.spotify.com/api/token'
    # POST
    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': SPOTIPY_CLIENT_ID,
        'client_secret': SPOTIPY_CLIENT_SECRET,
    })
    
    # convert the response to JSON
    auth_response_data = auth_response.json()
    
    # save the access token
    access_token = auth_response_data['access_token']
    headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
    }
    # base URL of all Spotify API endpoints
    BASE_URL = 'https://api.spotify.com/v1/'
    if emotion == 'angry':
        my_playlist_id = "43hZ7FIkem23HC0YUlJMdP"
    elif emotion == 'disgust':
        my_playlist_id = "134QDioEojAkcr9t1ZJdY4"
    elif emotion == 'fear':
        my_playlist_id = "2NNRjGHh0AhqZZUKMfzK2L"
    elif emotion == 'happy':
        my_playlist_id = "6xdiJLCEmwtGIdLUm7ovyh"
    elif emotion == 'sad':
        my_playlist_id = "1thDrHvEiDWWaZhIyU9mvv"
    elif emotion == 'surprise':
        my_playlist_id = "4PC1GWhuK86IkqL4Yey9vC"   
    elif emotion == 'neutral':
        my_playlist_id = "60fdyPFFApxLb1j0Egcxdt"
    else:
        my_playlist_id = "6SwsPEksv2o84OVqNUNZp6"
    responsed = requests.get(BASE_URL+"playlists/"+my_playlist_id+"/tracks",headers=headers)
    myplaylists = responsed.json()
    print(len(myplaylists.get('items')))
    song=random.randint(0,len(myplaylists.get('items'))-1)
    external_url = myplaylists.get('items')[song].get('track').get('external_urls').get('spotify')
    return JsonResponse({"url":external_url, "emotion":emotion})