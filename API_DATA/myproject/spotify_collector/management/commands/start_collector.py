from django.core.management.base import BaseCommand
import subprocess
import webbrowser
from django.conf import settings
import os
from dotenv import load_dotenv

load_dotenv()

class Command(BaseCommand):
    help = 'Starts the Spotify Data Collector Script'
    
    def handle(self, *args, **kwargs):
        client_id = os.getenv('SPOTIPY_CLIENT_ID')
        redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')
        scopes 
        self.stdout.write(self.style.SUCCESS('Starting Spotify Data Collector...'))
        subprocess.run(['python3', '/Users/spencerpresley/HenHacks/Spotify_WrapUp_Plus/API_DATA/spotify_data_collector.py'])
        self.stdout.write(self.style.SUCCESS('Spotify data collector finished.'))