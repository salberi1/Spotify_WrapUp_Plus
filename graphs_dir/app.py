from flask import Flask, render_template
import plotly.express as px
import plotly.io as pio
from io import BytesIO
import base64

app = Flask(__name__)

@app.route('/')
def index():
    # Generate Plotly figure (replace this with your own graph generation logic)
    fig = px.scatter(x=[1, 2, 3, 4], y=[10, 11, 12, 13], labels={'x': 'X-axis', 'y': 'Y-axis'}, title='My Plot')

    # Convert Plotly figure to HTML representation
    graph_html = pio.to_html(fig, full_html=False)

    return render_template('index.html', graph_html=graph_html)

if __name__ == '__main__':
    app.run(debug=True)
