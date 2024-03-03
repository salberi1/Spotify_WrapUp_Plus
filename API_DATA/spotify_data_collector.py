from authenticator import Authenticator
import pandas as pd
import os
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import threading

class SpotifyAuthentication():
    def __init__(self):
        self.auth = Authenticator()
        
    def initiate_authentication(self):
        auth_instance = Authenticator()
        auth_url = auth_instance.sp_oauth.get_authorize_url()
        print(f"navigate to {auth_url}")
        response_url = input("enter the url you were redirected to: ")
        return auth_instance, response_url
    
    def authenticate(self, response_url):
        self.auth.authenticate_user(response_url=response_url)
        sp = self.auth.get_authenticated_instance()
        return sp

class GetSpotifyData:
    def __init__(self, sp):
        self.sp = sp
    
    def _fetch_with_pagination(self, fetch_function, *args, **kwargs):
        items = []
        page: int = 1
        while True:
            try:
                results = fetch_function(*args, **kwargs)
                items.extend(results['items'])
                print(f"Fetched page {page} ({len(items)}) items so far)")
                page += 1
                if not results['next']:
                    break
                kwargs['offset'] += len(results['items'])
            except spotipy.exceptions.SpotifyException as e:
                if e.http_status == 429:
                    retry_after = int(e.headers['Retry-After'])
                    print(f"Rate limit exceeded. Retrying after {retry_after} seconds.")
                    time.sleep(retry_after + 1)
                else:
                    raise e
        return items

    def _fetch_followed_artists_with_cursor_pagination(self):
        followed_artists = []
        after = None  # Cursor initialization

        while True:
            try:
                # Fetch followed artists using cursor-based pagination
                results = self.sp.current_user_followed_artists(limit=50, after=after)
                followed_artists.extend(results['artists']['items'])

                # Spotify provides a 'cursors' object, which contains the 'after' key for pagination
                if not results['artists']['cursors']['after']:
                    break  # Exit the loop if there's no more artists to fetch

                # Update the 'after' cursor for the next iteration
                after = results['artists']['cursors']['after']

            except spotipy.exceptions.SpotifyException as e:
                if e.http_status == 429:
                    retry_after = int(e.headers['Retry-After'])
                    print(f"Rate limit exceeded. Retrying after {retry_after} seconds.")
                    time.sleep(retry_after + 1)
                else:
                    raise e

        return followed_artists        

    def _fetch_recently_played_with_pagination(self):
        items = []
        limit = 50
        last_timestamp = None  # Initialize the last timestamp variable

        while True:
            try:
                if last_timestamp:
                    # If we have a timestamp, fetch tracks played before this timestamp
                    results = self.sp.current_user_recently_played(limit=limit, before=last_timestamp)
                else:
                    # For the first call, no before parameter is needed
                    results = self.sp.current_user_recently_played(limit=limit)
                
                new_items = results['items']
                if not new_items:
                    break  # Exit if no more items are returned
                
                items.extend(new_items)
                # Update last_timestamp with the timestamp of the last track fetched
                last_timestamp = new_items[-1]['played_at']

            except spotipy.exceptions.SpotifyException as e:
                if e.http_status == 429:
                    retry_after = int(e.headers['Retry-After'])
                    print(f"Rate limit exceeded. Retrying after {retry_after} seconds.")
                    time.sleep(retry_after + 1)
                else:
                    raise e

        return items
               
    def get_saved_tracks(self):
        #return self.sp.current_user_saved_tracks()
        saved_tracks = self._fetch_with_pagination(self.sp.current_user_saved_tracks, limit=50, offset=0)
        print(f"\n\n\n{saved_tracks}\n\n\n")
        return saved_tracks
    def get_top_tracks_short(self):
        #return self.sp.current_user_top_tracks(time_range='short_term')
        return self._fetch_with_pagination(self.sp.current_user_top_tracks, time_range='short_term', limit=50, offset=0)
        
    def get_top_tracks_medium(self):
        #return self.sp.current_user_top_tracks(time_range='medium_term')
        return self._fetch_with_pagination(self.sp.current_user_top_tracks, time_range='medium_term', limit=50, offset=0)
    
    def get_top_tracks_long(self):
        #return self.sp.current_user_top_tracks(time_range='long_term')
        return self._fetch_with_pagination(self.sp.current_user_top_tracks, time_range='long_term', limit=50, offset=0)
    
    def get_recent_played(self):
        #return self.sp.current_user_recently_played(limit=50)
        return self._fetch_recently_played_with_pagination()
    
    def get_top_artists_short(self):
        #return self.sp.current_user_top_artists(time_range='short_term')
        return self._fetch_with_pagination(self.sp.current_user_top_artists, time_range='short_term', limit=50, offset=0)
    
    def get_top_artists_medium(self):
        #return self.sp.current_user_top_artists(time_range='medium_term')
        return self._fetch_with_pagination(self.sp.current_user_top_artists, time_range='medium_term', limit=50, offset=0)    
    
    def get_top_artists_long(self):
        #return self.sp.current_user_top_artists(time_range='long_term')
        return self._fetch_with_pagination(self.sp.current_user_top_artists, time_range='long_term', limit=50, offset=0)
    
    def get_playlists(self):
        #return self.sp.current_user_playlists(limit=50)
        return self._fetch_with_pagination(self.sp.current_user_playlists, limit=50, offset=0)
    
    def get_followed_artists(self):
        #return self.sp.current_user_followed_artists(limit=50)
        return self._fetch_followed_artists_with_cursor_pagination()
    
    def process_and_save_data(self, results):
        for item in results['items']:
            track = item['track']
            self.data_list.append({
                'Artist': track['artists'][0]['name'],
                'Song': track['name'],
                'Album': track['album']['name'],
                'Release Date': track['album']['release_date']
            })
            
        self.df = pd.DataFrame(self.data_list)
        self.df.to_csv('user_data.csv', index=False)
        self.df.to_json('user_data.json', orient='records', lines=True)
        print(self.df.head())

    def get_authentication(self):
        auth_instance, response_url = self.initiate_authentication()
        results = self.authenticate_and_fetch_data(auth_instance, response_url)
        self.process_and_save_data(results)
        
class ProcessSpotifyData():
    """Uses GetSpotifyData to retrieve data and stores it in dataframes"""
    def __init__(self, sp):
        self.sp = sp
        self.sp_data_getter = GetSpotifyData(sp=self.sp)
        
        # dictionary to store dataframes. Key: type of data, Value: the dataframe for the data
        self.data_frames_dict = {}
    
    def get_data(self):
        threads = []
        
        methods = [
            self.process_saved_tracks(),
            self.process_top_artists_short(),
            self.process_top_artists_medium(),
            self.process_top_artists_long(),
            self.process_top_tracks_short(),
            self.process_top_tracks_medium(),
            self.process_top_tracks_long(),
            self.process_recently_played(),
            self.process_playlists(),
            self.process_followed_artists()
        ]
        
        for method in methods:
            thread = threading.Thread(target=method)
            threads.append(thread)
            thread.start()
            
        for thread in threads:
            thread.join()
        
        print("Saving DataFrames to CSVs")
        self.df_to_csv()
        print("\n\n\nSaving DataFrames to JSONs")
        self.df_to_json()
        print("\n\n\nDone")
        
    def df_to_csv(self):
        dir_name = 'data_csvs'
        
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            
        for key, df in self.data_frames_dict.items():
            file_name = f"{dir_name}/{key}.csv"
            df.to_csv(file_name, index=False)
            print(f"Saved {file_name}")
    
    def df_to_json(self):
        dir_name = 'data_jsons'
        
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            
        for key, df in self.data_frames_dict.items():
            file_name = f"{dir_name}/{key}.json"
            df.to_json(file_name, orient='records', lines=True)
            print(f"Saved {file_name}")
    
    def process_saved_tracks(self):
        data_list = []
        saved_tracks = self.sp_data_getter.get_saved_tracks()
        # print("First 10 Saved Tracks:")
        # for i, item in enumerate(saved_tracks['items'][:10]):
        #     track = item['track']
        #     print(f"{i+1}. Artist: {track['artists'][0]['name']}, Song: {track['name']}")
        for track_info in saved_tracks:
            track = track_info['track']
            data_list.append({
                'Artist': track['artists'][0]['name'],
                'Song': track['name'],
                'Album': track['album']['name'],
                'Release Date': track['album']['release_date']
            })
        saved_tracks_df = pd.DataFrame(data_list)
        self.data_frames_dict['saved_tracks'] = saved_tracks_df
        
    def process_top_tracks_short(self):
        data_list = []
        top_tracks_short = self.sp_data_getter.get_top_tracks_short()
        for item in top_tracks_short:
            track = item
            data_list.append({
                'Term': 'short_term',
                'Artist': track['artists'][0]['name'],
                'Song': track['name'],
                'Album': track['album']['name'],
                'Release Date': track['album']['release_date']
            })
        top_tracks_short_df = pd.DataFrame(data_list)
        self.data_frames_dict['top_tracks_short'] = top_tracks_short_df

    def process_top_tracks_medium(self):
        data_list = []
        top_tracks_med = self.sp_data_getter.get_top_tracks_medium()
        for item in top_tracks_med:
            track = item
            data_list.append({
                'Term': 'medium_term',
                'Artist': track['artists'][0]['name'],
                'Song': track['name'],
                'Album': track['album']['name'],
                'Release Date': track['album']['release_date']
            })
        top_tracks_medium_df = pd.DataFrame(data_list)
        self.data_frames_dict['top_tracks_medium'] = top_tracks_medium_df

    def process_top_tracks_long(self):
        data_list = []
        top_tracks_long = self.sp_data_getter.get_top_tracks_long()
        for item in top_tracks_long:
            track = item
            data_list.append({
                'Term': 'long_term',
                'Artist': track['artists'][0]['name'],
                'Song': track['name'],
                'Album': track['album']['name'],
                'Release Date': track['album']['release_date']
            })
        top_tracks_long_df = pd.DataFrame(data_list)
        self.data_frames_dict['top_tracks_long'] = top_tracks_long_df
        
    def process_recently_played(self):
        data_list = []
        recently_played = self.sp_data_getter.get_recent_played()
        for item in recently_played:
            track = item['track']
            data_list.append({
                'Artist': track['artists'][0]['name'],
                'Song': track['name'],
                'Played At': item['played_at']
            })
        recently_played_df = pd.DataFrame(data_list)
        self.data_frames_dict['recently_played'] = recently_played_df
        
    def process_top_artists_short(self):
        data_list = []
        top_artists_short = self.sp_data_getter.get_top_artists_short()
        for artist in top_artists_short:
            data_list.append({
                'Term': 'short_term',
                'Artist': artist['name'],
                'Genres': ', '.join(artist['genres']),
                'Popularity': artist['popularity']
            })
        top_artists_short_df = pd.DataFrame(data_list)
        self.data_frames_dict['top_artists_short'] = top_artists_short_df
        
    def process_top_artists_medium(self):
        data_list = []
        top_artists_medium = self.sp_data_getter.get_top_artists_medium()
        for artist in top_artists_medium:
            data_list.append({
                'Term': 'medium_term',
                'Artist': artist['name'],
                'Genres': ', '.join(artist['genres']),
                'Popularity': artist['popularity']
            })
        top_artists_medium_df = pd.DataFrame(data_list)
        self.data_frames_dict['top_artists_medium'] = top_artists_medium_df    
        
    def process_top_artists_long(self):
        data_list = []
        top_artists_long = self.sp_data_getter.get_top_artists_long()
        for artist in top_artists_long:
            data_list.append({
                'Term': 'long_term',
                'Artist': artist['name'],
                'Genres': ', '.join(artist['genres']),
                'Popularity': artist['popularity']
            })
        top_artists_long_df = pd.DataFrame(data_list)
        self.data_frames_dict['top_artists_long'] = top_artists_long_df
        
    def process_playlists(self):
        data_list = []
        playlists = self.sp_data_getter.get_playlists()
        for item in playlists:
            data_list.append({
                'Playlist Name': item['name'],
                'Owner': item['owner']['display_name'],
                'Total Tracks': item['tracks']['total']
            })
        playlists_df = pd.DataFrame(data_list)
        self.data_frames_dict['playlists'] = playlists_df                     
    
    def process_followed_artists(self):
        data_list = []
        followed_artists = self.sp_data_getter.get_followed_artists()
        for artist in followed_artists:
            data_list.append({
                'Artist': artist['name'],
                'Genres': ', '.join(artist['genres']),
                'Popularity': artist['popularity']
            })
        followed_artists_df = pd.DataFrame(data_list)
        self.data_frames_dict['followed_artists'] = followed_artists_df
    
if __name__ == "__main__":
    # spotify_auth = SpotifyAuthentication()
    
    # auth_instance, response_url = spotify_auth.initiate_authentication()
    # sp = spotify_auth.authenticate(response_url=response_url)
    
    # spotify_data = ProcessSpotifyData(sp=sp)
    # spotify_data.get_data()
    print("hello")
    
print("hello2")