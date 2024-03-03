from flask import Flask, render_template
import pandas as pd
import plotly.express as px
import plotly.io as pio
from io import BytesIO
import base64
import subprocess
import os



app = Flask(__name__)

# @app.route('/')
# def index():
#     # Generate Plotly figure (replace this with your own graph generation logic)
#     #fig = px.scatter(x=[1, 2, 3, 4], y=[10, 11, 12, 13], labels={'x': 'X-axis', 'y': 'Y-axis'}, title='My Plot')
#     import plotly.express as px

#     df = pd.read_csv('/Users/spencerpresley/HenHacks/Spotify_WrapUp_Plus/API_DATA/data_csvs/saved_tracks.csv') 
#     artist = df['Artist'].value_counts(sort=True)
#     number_of_artist= pd.DataFrame(artist)
#     number_of_artist.reset_index(inplace=True)
#     number_of_artist.columns = ['Artists', 'Listens']
#     fig = px.bar(number_of_artist, x="Artists", y="Listens", title="Number of Listens by Artist", range_y=[0,5])

#     # Convert Plotly figure to HTML representation
#     graph_html = pio.to_html(fig, full_html=False)

#     return render_template('index2.html', graph_html=graph_html)

@app.route('/')
def index():
    # Call spotify_data_collector.py and wait for it to complete
    if os.path.exists('./data_csvs') and len(os.listdir('./data_csvs')) > 0:
        print("Data already exists. Skipping data collection.")
    else:
        result = subprocess.run(['python3', '../API_DATA/spotify_data_collector.py'], check=True)
        print(result.stdout)
        print(result.stderr)
    # Now that spotify_data_collector.py has completed, load the CSV
    df = pd.read_csv('./data_csvs/saved_tracks.csv')
    artist = df['Artist'].value_counts(sort=True)
    number_of_artist = pd.DataFrame(artist)
    number_of_artist.reset_index(inplace=True)
    number_of_artist.columns = ['Artists', 'Listens']
    
    # Generate the Plotly figure
    fig = px.bar(number_of_artist, x="Artists", y="Listens", title="Number of Listens by Artist", range_y=[0,5])

    # Convert Plotly figure to HTML representation
    graph_html = pio.to_html(fig, full_html=False)

    # Render the template with the graph
    return render_template('index2.html', graph_html=graph_html)

@app.route('/run_spotify_collector', methods=['POST'])
def run_spotify_collector():
    subprocess.run(['python3', '../API_DATA/spotify_data_collector.py'])
    return "Spotify data collection initiated."

if __name__ == '__main__':
    app.run(debug=True)
