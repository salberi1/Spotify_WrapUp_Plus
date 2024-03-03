from django.core.management.base import BaseCommand
import webbrowser
from django.conf import settings
import subprocess

class Command(BaseCommand):
    help = 'Starts the Spotify OAuth flow by opening the authentication URL in the default web browser.'

    def handle(self, *args, **kwargs):
        client_id = settings.SPOTIFY_CLIENT_ID
        redirect_uri = settings.SPOTIFY_REDIRECT_URI
        scopes = 'user-read-private user-read-email'  # Adjust based on your needs

        # Construct the Spotify authentication URL
        auth_url = f"https://accounts.spotify.com/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope={scopes}"

        # Open the authentication URL in the default web browser
        webbrowser.open(auth_url)
        self.stdout.write(self.style.SUCCESS('Opened Spotify authentication page in your browser. Please log in and authorize access.'))

        # If the subprocess call is part of your workflow, ensure the script path is correct and consider security implications
        subprocess.run(['python3', '/path/to/spotify_data_collector.py'])
        self.stdout.write(self.style.SUCCESS('Spotify data collector finished.'))