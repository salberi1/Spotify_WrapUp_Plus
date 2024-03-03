import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import os

class DataVisualization:
    def __init__(self):
        self.followed_artist_path = './data_csvs/followed_artists.csv'
        self.playlists_path = './data_csvs/playlists.csv'
        self.recently_played_path = './data_csvs/recently_played.csv'
        self.saved_tracks_path = './data_csvs/saved_tracks.csv'
        self.top_artists_long_path = './data_csvs/top_artists_long.csv'
        self.top_artists_medium_path = './data_csvs/top_artists_medium.csv'
        self.top_artists_short_path = './data_csvs/top_artists_short.csv'
        self.top_tracks_long_path = './data_csvs/top_tracks_long.csv'
        self.top_tracks_medium_path = './data_csvs/top_tracks_medium.csv'
        self.top_tracks_short_path = './data_csvs/top_tracks_short.csv'
        self.graphs_dir = '/Users/spencerpresley/HenHacks/Spotify_WrapUp_Plus/graphs_dir'
        
    def followed_artists_visualization(self):
        df = pd.read_csv(self.followed_artist_path)
        
        # count num of genres per artist
        df['Genres Count'] = df['Genres'].apply(lambda x: len(str(x).split(',')) if not pd.isna(x) else 0)
        
        # create a bubble chart
        fig = px.scatter(df, x='Artist', y='Popularity',
                        size='Popularity', color='Genres Count',
                        hover_name='Artist', hover_data=['Genres'], 
                        title='Artists Popularity and Genre Diversity', 
                        color_continuous_scale=px.colors.sequential.Plasma)
        
        # imporve layout
        fig.update_layout(
            xaxis=dict(
                categoryorder='total descending',
                gridcolor='rgba(80,80,80,0.5)',
                title=dict(text='Artist')  # Assuming you want to set a title for the x-axis
            ),
            yaxis=dict(
                gridcolor='rgba(80,80,80,0.5)',
                title=dict(
                    text='Popularity',  # Correct way to set the y-axis title
                    font=dict(color='white')  # Example of setting the font color for the y-axis title
                )
            ),
            plot_bgcolor='rgba(10,10,10,1)',  
            paper_bgcolor='rgba(35,35,35,1)',  
            font=dict(color='white')  
        )
        
        fig.update_traces(
            marker=dict(
                symbol='diamond',  # Change shape to diamond
                size=18,  # Adjust size as needed
                line=dict(width=2, color='DarkSlateGrey'),  # Add a border to the markers
            ),
            opacity=1.0  # Adjust opacity to make points stand out
        )
        
        fig.show()
        fig.write_html(os.path.join(self.graphs_dir, "followed_artists_visualization.html"))
        
    def playlists_visualization(self):
        df = pd.read_csv(self.playlists_path)
        
        # Counting the number of playlists per owner for the pie chart
        owner_playlist_count = df['Owner'].value_counts()

        # Creating the pie chart with custom aesthetics
        fig = go.Figure(go.Pie(labels=owner_playlist_count.index, values=owner_playlist_count.values, hoverinfo='label+percent'))

        # Setting the title and improving layout to match the provided aesthetics
        fig.update_layout(
            title_text='Distribution of Playlists by Owner',
            plot_bgcolor='rgba(10,10,10,1)',  # Setting plot background color
            paper_bgcolor='rgba(35,35,35,1)',  # Setting overall background color of the chart area
            font=dict(color='white'),  # Setting font color to white for all text in the chart
            legend=dict(
                traceorder='normal',
                font=dict(
                    family='sans-serif',
                    size=12,
                    color='white'
                ),
                bgcolor='rgba(35,35,35,1)'
            )
        )

        # Adjusting the pie chart color scale to match the Plasma theme from your scatter plot
        fig.update_traces(marker=dict(colors=px.colors.sequential.Plasma, line=dict(color='#000000', width=2)))

        # Display the figure
        fig.show()        
        fig.write_html(os.path.join(self.graphs_dir, "playlists_visualization.html"))
        
    def playlist_recent_top_track_overlap(self):
        recent_df = pd.read_csv(self.recently_played_path)
        top_tracks_l_df = pd.read_csv(self.top_tracks_long_path)
        top_tracks_m_df = pd.read_csv(self.top_tracks_medium_path)
        top_tracks_s_df = pd.read_csv(self.top_tracks_short_path)
        unique_recently_played, unique_top_tracks, overlap_tracks = self.calculate_overlap(recent_df, top_tracks_l_df, top_tracks_m_df, top_tracks_s_df)   

        fig = go.Figure()
        # Add the bar for unique recently played tracks
        fig.add_trace(go.Bar(x=['Unique Recently Played'], y=[unique_recently_played], name='Unique Recently Played'))
        # Add the bar for unique top tracks
        fig.add_trace(go.Bar(x=['Unique Top Tracks'], y=[unique_top_tracks], name='Unique Top Tracks'))
        # Add the bar for the overlap
        fig.add_trace(go.Bar(x=['Overlap'], y=[overlap_tracks], name='Overlap'))
        
        # Customize the layout
        fig.update_layout(
            title='Overlap Between Recently Played and Top Tracks',
            plot_bgcolor='rgba(10,10,10,0.95)',  # dark plot background color
            paper_bgcolor='rgba(25,25,25,0.95)',  # dark paper background color
            font=dict(color='rgba(220,220,220,0.95)'),  # light font color for contrast
            xaxis=dict(
                title='Categories',  # X-axis title
                tickangle=-45,  # Angle the x-axis labels for better readability
                title_standoff=25  # Distance of axis title from the axis
            ),
            yaxis=dict(
                title='Track Count',  # Y-axis title
                gridcolor='rgba(80,80,80,0.5)'  # Lighter grid lines for subtle contrast
            ),
            legend=dict(
                title='Legend',  # Legend title
                bgcolor='rgba(50,50,50,0.6)',  # Semi-transparent background for the legend
                bordercolor='rgba(255,255,255,0.2)',  # Light border for the legend
                font=dict(
                    color='rgba(200,200,200,0.95)'  # Light font color for the legend text
                )
            ),
            barmode='group'  # Grouped bar mode to show bars side by side
        )

        # Adding a color theme to the bars for visual appeal
        fig.update_traces(marker_color=['rgba(255,127,80,0.6)', 'rgba(31,119,180,0.6)', 'rgba(44,160,44,0.6)'])

        # Show the plot
        fig.show()
        fig.write_html(os.path.join(self.graphs_dir, "playlists_recent_top_tracks.html"))


        
    def calculate_overlap(self, recent_df, top_tracks_l_df, top_tracks_m_df, top_tracks_s_df):
        recent = recent_df['Artist'] + ' - ' + recent_df['Song']
        top_t_l = top_tracks_l_df['Artist'] + ' - ' + top_tracks_l_df['Song']
        top_t_m = top_tracks_m_df['Artist'] + ' - ' + top_tracks_m_df['Song']
        top_t_s = top_tracks_s_df['Artist'] + ' - ' + top_tracks_s_df['Song']
        
        # Combine all top tracks into a set for unique comparison
        top_tracks_set = set(top_t_l) | set(top_t_m) | set(top_t_s)
        recent_set = set(recent)
        
        # Calculating the unique and overlapping tracks
        unique_recently_played = len(recent_set - top_tracks_set)
        unique_top_tracks = len(top_tracks_set - recent_set)
        overlap_tracks = len(recent_set & top_tracks_set)
        
        return unique_recently_played, unique_top_tracks, overlap_tracks 
     
    def top_artists_visualization(self):
        # Load data from all three time frames
        top_tracks_l_df = pd.read_csv(self.top_tracks_long_path)
        top_tracks_m_df = pd.read_csv(self.top_tracks_medium_path)
        top_tracks_s_df = pd.read_csv(self.top_tracks_short_path)

        # Combine the dataframes
        combined_df = pd.concat([top_tracks_l_df, top_tracks_m_df, top_tracks_s_df])

        # Count the occurrences of each artist
        artist_counts = combined_df['Artist'].value_counts().head(50)  # Limiting to top 50 for clarity

        # Define a custom discrete color sequence
        custom_colors = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', 
                         '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', 
                         '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000', 
                         '#aaffc3', '#808000', '#ffd8b1', '#000075', '#808080', 
                         '#ffffff', '#000000']

        # Repeat the color sequence if there are more artists than colors
        colors = custom_colors * (len(artist_counts) // len(custom_colors) + 1)

        # Create the bar chart with the custom color sequence
        fig = px.bar(artist_counts, x=artist_counts.index, y=artist_counts.values, 
                    title="Top 50 Artists Across All Time Frames",
                    labels={'x': 'Artist', 'y': 'Number of Songs'},
                    color_discrete_sequence=colors[:len(artist_counts)])  # Use the custom color sequence here

        # Update the layout
        fig.update_layout(plot_bgcolor='rgba(10,10,10,0.95)',  
                          paper_bgcolor='rgba(10,10,10,1)',  
                          font=dict(color='white', family="Arial, sans-serif"),
                          title_font=dict(size=24, color='rgba(255,255,255,0.9)'),
                          legend_title_font_color="rgba(255,255,255,0.9)",
                          legend=dict(
                              orientation="h",
                              yanchor="bottom",
                              y=1.02,
                              xanchor="right",
                              x=1
                          ))
        fig.update_xaxes(tickangle=-45, tickfont=dict(family='Arial, sans-serif', color='lightgrey', size=12))
        fig.update_yaxes(tickfont=dict(family='Arial, sans-serif', color='lightgrey', size=12))

        # Show the plot
        fig.show()
        fig.write_html(os.path.join(self.graphs_dir, "top_artists.html"))

    def play_times_distribution_visualization(self):
        df = pd.read_csv(self.recently_played_path)
        df['Played At'] = pd.to_datetime(df['Played At'])
        df['Hour of Day'] = df['Played At'].dt.hour

        # Simplify the conversion of 'Hour of Day' to 'Time of Day' in 12-hour format with AM/PM
        df['Time of Day'] = df['Hour of Day'].apply(lambda x: f"{x%12 if x%12 else 12}:00 {'AM' if x < 12 else 'PM'}")

        # Ensure all 24 hours are represented
        all_hours = [f"{i%12 if i%12 else 12}:00 {'AM' if i < 12 else 'PM'}" for i in range(24)]

        # Define a custom discrete color sequence
        custom_colors = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', 
                         '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', 
                         '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000', 
                         '#aaffc3', '#808000', '#ffd8b1', '#000075', '#808080', 
                         '#ffffff', '#000000']

        # Repeat the color sequence if there are more bins than colors
        colors = custom_colors * (24 // len(custom_colors) * (24 // len(custom_colors) + 1))

        # Create the histogram with the custom color sequence
        fig = px.histogram(df, x='Time of Day', 
                           title='Distribution of Play Times Throughout the Day',
                           labels={'Time of Day': 'Time of the Day'},
                           category_orders={'Time of Day': all_hours},
                           color_discrete_sequence=colors[:10])  # Use the custom color sequence here

        # Update the layout
        fig.update_layout(plot_bgcolor='rgba(10,10,10,1)',  
                          paper_bgcolor='rgba(35,35,35,1)',  
                          font=dict(color='white', family="Arial, sans-serif"),
                          xaxis=dict(title='Time of the Day', title_font=dict(size=16, family='Arial, sans-serif', color='rgba(255,255,255,0.9)')),
                          yaxis=dict(title='Number of Songs Played', title_font=dict(size=16, family='Arial, sans-serif', color='rgba(255,255,255,0.9)')),
                          title_font=dict(size=24, color='rgba(255,255,255,0.9)', family="Arial, sans-serif"),
                          legend_title_font_color="rgba(255,255,255,0.9)",
                          legend=dict(
                              orientation="h",
                              yanchor="bottom",
                              y=1.02,
                              xanchor="right",
                              x=1
                          ))
        fig.update_xaxes(tickangle=-45, tickfont=dict(family='Arial, sans-serif', color='lightgrey', size=12), categoryorder='array', categoryarray=all_hours)
        fig.update_yaxes(tickfont=dict(family='Arial, sans-serif', color='lightgrey', size=12))

        # Show the plot
        fig.show()
        fig.write_html(os.path.join(self.graphs_dir, "play_time_distribution.html"))
        
    def listening_trends_over_time(self):
        df = pd.read_csv(self.saved_tracks_path)
        
        df['Release Date'] = pd.to_datetime(df['Release Date'], errors='coerce')
        
        df['Year'] = df['Release Date'].dt.year
        tracks_per_year = df.groupby('Year').size().reset_index(name='Tracks')

        # Find the era with the most tracks
        era_counts = tracks_per_year.groupby((tracks_per_year['Year']//10)*10).sum()
        most_popular_era = era_counts['Tracks'].idxmax()
        
        # Determine the user's preferred era
        if most_popular_era < 1980:
            era_name = 'Classics Era'
        elif most_popular_era == 1980:
            era_name = '80s Era'
        elif most_popular_era == 1990:
            era_name = '90s Era'
        elif most_popular_era == 2000:
            era_name = '2000s Era'
        elif most_popular_era == 2010:
            era_name = '2010s Era'
        else:
            era_name = 'Modern Era'

        # Customize the title with the user's preferred era
        title = f'You\'re in your {era_name}!'

        fig = px.line(tracks_per_year, x='Year', y='Tracks', markers=True, title=title)
        fig.update_layout(plot_bgcolor='rgba(10,10,10,1)', paper_bgcolor='rgba(35,35,35,1)', font=dict(color='white'))
        fig.update_xaxes(gridcolor='rgba(80,80,80,0.2)')
        fig.update_yaxes(gridcolor='rgba(80,80,80,0.2)')
        fig.update_xaxes(title_text='Year', gridcolor='rgba(80,80,80,0.5)')
        fig.update_yaxes(title_text='Number of Tracks Saved', gridcolor='rgba(80,80,80,0.5)')
        fig.show()
        fig.write_html(os.path.join(self.graphs_dir, "listening_trends.html"))

       
    def recently_played_visualization(self):
        # Load the recently played data
        df = pd.read_csv(self.recently_played_path)
        df['Played At'] = pd.to_datetime(df['Played At'])
        df['Year'] = df['Played At'].dt.year

        # Aggregate data by year and artist
        artist_listening_counts_per_year = df.groupby(['Year', 'Artist']).size().reset_index(name='Listening Sessions')
        artist_listening_counts_per_year = artist_listening_counts_per_year.sort_values(['Year', 'Listening Sessions'], ascending=[True, False])

        # Assuming we're visualizing for the most recent year in the dataset
        recent_year = artist_listening_counts_per_year['Year'].max()
        recent_year_data = artist_listening_counts_per_year[artist_listening_counts_per_year['Year'] == recent_year]

        # Visualize the top artists for the recent year
        fig = px.bar(recent_year_data.head(10), x='Artist', y='Listening Sessions', color='Listening Sessions', 
                     title=f'Top Artists Listened to in {recent_year}', 
                     labels={'Listening Sessions': 'Number of Listening Sessions'},
                     color_continuous_scale=px.colors.sequential.Viridis)

        fig.update_layout(xaxis_title='Artist', yaxis_title='Listening Sessions',
                          plot_bgcolor='rgba(112,128,144,1)', # Slate Gray background
                          paper_bgcolor='rgba(112,128,144,1)', # Slate Gray background
                          font=dict(color='white'), # White, bold text
                          xaxis=dict(showgrid=False), # No grid lines for x-axis
                          yaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.5)')) # White grid lines for y-axis

        fig.show()
        fig.write_html(os.path.join(self.graphs_dir, "recently_played.html"))
        
if __name__ == "__main__":
    data_vis = DataVisualization()
    data_vis.followed_artists_visualization()
    data_vis.playlists_visualization()
    data_vis.playlist_recent_top_track_overlap()
    data_vis.top_artists_visualization()
    data_vis.play_times_distribution_visualization()
    data_vis.listening_trends_over_time()
    data_vis.recently_played_visualization()