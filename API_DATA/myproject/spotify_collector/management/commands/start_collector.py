from django.core.management.base import BaseCommand
import subprocess

class Command(BaseCommand):
    help = 'Starts the Spotify Data Collector Script'
    
    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting Spotify Data Collector...'))
        subprocess.run(['python3', '/Users/spencerpresley/HenHacks/Spotify_WrapUp_Plus/API_DATA/spotify_data_collector.py'])
        self.stdout.write(self.style.SUCCESS('Spotify data collector finished.'))