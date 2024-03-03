from django.shortcuts import render

# Create your views here.
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
import requests
from dotenv import load_dotenv
load_dotenv()
import os

def spotify_callback(request):
    code = requests.GET.get('code')
    if code:
        token_url = 'https://accounts.spotify.com/api/token'
        redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')
        client_id = os.getenv('SPOTIPY_CLIENT_ID')
        client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
        
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_uri,
            'client_id': client_id,
            'client_secret': client_secret,
        }
        
        response = requests.post(token_url, data=data)
        if response.status_code == 200:
            access_token_info = response.json()
            access_token = access_token_info['access_token']
            return HttpResponse("Authetication success. You can close this window.")
        else:
            return HttpResponse("No code provided.")
        