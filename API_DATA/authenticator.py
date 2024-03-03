import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

class Authenticator:
    def __init__(self):
        load_dotenv()
        self.scope = "user-library-read"
        self.client_id = os.getenv('SPOTIPY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
        self.redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')
        self.sp_oauth = SpotifyOAuth(scope=self.scope,
                                     client_id=self.client_id,
                                     client_secret=self.client_secret,
                                     redirect_uri=self.redirect_uri)
        self.sp = None
        
    def authenticate_user(self, response_url):
        code = self.sp_oauth.parse_response_code(response_url)
        token_info = self.sp_oauth.get_access_token(code)
        self.sp = spotipy.Spotify(auth=token_info['access_token'])
        
    def get_authenticated_instance(self):
        if self.sp is not None:
            return self.sp
        else:
            raise Exception("User not yet authenticated.  Call authenticate_user() with the response URL first.")

