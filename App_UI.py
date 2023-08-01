from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from spotipy.oauth2 import SpotifyOAuth
import spotipy

class SpotifyWrapperApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="2bd3abf122f54dd0b16eedfa81d2160c",
                                               client_secret="be6572cfc34e48e6a16c49b1eaf87929",
                                               redirect_uri="http://localhost:3000",
                                               scope="user-library-read"))


    def get_most_tracked_artists(self):
        results = self.spotify.current_user_top_artists(limit=10, time_range='medium_term')
        return results['items']

    def get_most_tracked_songs(self):
        results = self.spotify.current_user_top_tracks(limit=10, time_range='medium_term')
        return results['items']

    def build(self):
        layout = BoxLayout(orientation='vertical')

        button_layout = BoxLayout(orientation='horizontal')
        most_tracked_artists_button = Button(text='Most Tracked Artists', on_press=self.show_most_tracked_artists)
        most_tracked_songs_button = Button(text='Most Tracked Songs', on_press=self.show_most_tracked_songs)
        button_layout.add_widget(most_tracked_artists_button)
        button_layout.add_widget(most_tracked_songs_button)

        self.result_label = Label(text='')
        layout.add_widget(button_layout)
        layout.add_widget(self.result_label)

        return layout

    def show_most_tracked_artists(self, instance):
        artists = self.get_most_tracked_artists()
        self.show_results(artists)

    def show_most_tracked_songs(self, instance):
        songs = self.get_most_tracked_songs()
        self.show_results(songs)

    def show_results(self, items):
        result_text = ""
        for item in items:
            result_text += f"{item['name']} - {item['artists'][0]['name']}\n"
        self.result_label.text = result_text

SpotifyWrapperApp().run()
