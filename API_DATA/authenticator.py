import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

class Authenticator:
    def __init__(self):
        load_dotenv()
        self.scopes = "user-library-read user-top-read playlist-read-private user-follow-read user-read-recently-played user-read-playback-state"
        self.client_id = os.getenv('SPOTIPY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
        self.redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')
        self.sp_oauth = SpotifyOAuth(scope=self.scopes,
                                     client_id=self.client_id,
                                     client_secret=self.client_secret,
                                     redirect_uri=self.redirect_uri,
                                     cache_path='.cache')
        self.sp = None
        
    def get_authenticated_instance(self):
        return self.sp
    
    def authenticate_user(self, response_url):
        code = self.sp_oauth.parse_response_code(response_url)
        token_info = self.sp_oauth.get_access_token(code)
        self.sp = spotipy.Spotify(auth=token_info['access_token'])
        
    def get_authenticated_instance(self):
        if self.sp is not None:
            token_info = self.sp_oauth.get_cached_token()
            if token_info and self.sp_oauth.is_token_expired(token_info):
                print("Token expired. Refreshing...")
                new_token_info = self.sp_oauth.refresh_access_token(token_info['refresh_token'])
                self.sp = spotipy.Spotify(auth=new_token_info['access_token'])
            return self.sp
        else:
            raise Exception("User not yet authenticated.  Call authenticate_user() with the response URL first.")

