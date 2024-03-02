from authenticator import Authenticator
import pandas as pd
import os

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
    
    def get_saved_tracks(self):
        return self.sp.current_user_saved_tracks()
    
    def get_top_tracks_short(self):
        return self.sp.current_user_top_tracks(time_range='short_term')
    
    def get_top_tracks_medium(self):
        return self.sp.current_user_top_tracks(time_range='medium_term')
    
    def get_top_tracks_long(self):
        return self.sp.current_user_top_tracks(time_range='long_term')
    
    def get_recent_played(self):
        return self.sp.current_user_recently_played(limit=50)
    
    def get_top_artists_short(self):
        return self.sp.current_user_top_artists(time_range='short_term')
    
    def get_top_artists_medium(self):
        return self.sp.current_user_top_artists(time_range='medium_term')
    
    def get_top_artists_long(self):
        return self.sp.current_user_top_artists(time_range='long_term')
    
    def get_playlists(self):
        return self.sp.current_user_playlists(limit=50)
    
    def get_followed_artists(self):
        return self.sp.current_user_followed_artists(limit=50)
    
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
        self.process_saved_tracks()
        self.process_top_artists_short()
        self.process_top_artists_medium()
        self.process_top_artists_long()
        self.process_top_tracks_short()
        self.process_top_artists_medium()
        self.process_top_tracks_long()
        self.process_recently_played()
        self.process_playlists()
        self.process_followed_artists()
        
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
        for item in saved_tracks['items']:
            track = item['track']
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
        for item in top_tracks_short['items']:
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
        for item in top_tracks_med['items']:
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
        for item in top_tracks_long['items']:
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
        for item in recently_played['items']:
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
        for artist in top_artists_short['items']:
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
        for artist in top_artists_medium['items']:
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
        for artist in top_artists_long['items']:
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
        for item in playlists['items']:
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
        for artist in followed_artists['artists']['items']:
            data_list.append({
                'Artist': artist['name'],
                'Genres': ', '.join(artist['genres']),
                'Popularity': artist['popularity']
            })
        followed_artists_df = pd.DataFrame(data_list)
        self.data_frames_dict['followed_artists'] = followed_artists_df
        
if __name__ == "__main__":
    spotify_auth = SpotifyAuthentication()
    
    auth_instance, response_url = spotify_auth.initiate_authentication()
    sp = spotify_auth.authenticate(response_url=response_url)
    
    spotify_data = ProcessSpotifyData(sp=sp)
    spotify_data.get_data()
    
    
    