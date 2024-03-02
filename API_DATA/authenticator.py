import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

class authenticate:
    def __init__(self):
        load_dotenv()
        self.scope = "user-library-read"
        self.client_id = os.getenv('SPOTIPY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
        self.redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=self.scope,
                                                            client_id=self.client_id,
                                                            client_secret=self.client_secret,
                                                            redirect_uri=self.redirect_uri))
    
    def get_authentication(self):
        pass


