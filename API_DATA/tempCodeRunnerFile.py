   
def test_authentication():
    auth_instance = Authenticator()
    auth_url = auth_instance.sp_oauth.get_authorize_url()
    print(f"navigate to {auth_url}")
    response_url = input ("enter the url you were redirected to: ")
    auth_instance.authenticate_user(response_url=response_url)
    
    sp = auth_instance.get_authenticated_instance()
    results = sp.current_user_saved_tracks(limit=10)
    
    tracks_data = []
    for item in results['items']:
        track = item['track']
        tracks_data.append({
            'Artist': track['artists'][0]['name'],
            'Song': track['name'],
            'Album': track['album']['name'],
            'Release Date': track['album']['release_date']
        })
        
    df_tracks = pd.DataFrame(tracks_data)
    df_tracks.to_csv('user_data.csv', index=False)
    df_tracks.to_json('user_data.json', orient='records', lines=True)
    print(df_tracks.head())    
    
if __name__ == "__main__":
    test_authentication()