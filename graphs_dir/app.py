from flask import Flask, render_template
import pandas as pd
import plotly.express as px
import plotly.io as pio
from io import BytesIO
import base64



app = Flask(__name__)

@app.route('/')
def index():
    # Generate Plotly figure (replace this with your own graph generation logic)
    #fig = px.scatter(x=[1, 2, 3, 4], y=[10, 11, 12, 13], labels={'x': 'X-axis', 'y': 'Y-axis'}, title='My Plot')
    import plotly.express as px

    df = pd.read_csv(r'C:\Users\vince\Desktop\Spotify_WrapUp_Plus\API_DATA\user_data.csv') 
    artist = df['Artist'].value_counts(sort=True)
    number_of_artist= pd.DataFrame(artist)
    number_of_artist.reset_index(inplace=True)
    number_of_artist.columns = ['Artists', 'Listens']
    fig = px.bar(number_of_artist, x="Artists", y="Listens", title="Number of Listens by Artist", range_y=[0,5])

    # Convert Plotly figure to HTML representation
    graph_html = pio.to_html(fig, full_html=False)

    return render_template('index2.html', graph_html=graph_html)

if __name__ == '__main__':
    app.run(debug=True)
