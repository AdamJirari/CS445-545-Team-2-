import webbrowser
import urllib.parse

from unittest import result

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window

import spotipy
from spotipy.oauth2 import SpotifyOAuth

# from moviepy.editor import *


TIMEFRAME = 'medium_term'

class SpotifyWrapperApp(App):
    """main app class"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="2bd3abf122f54dd0b16eedfa81d2160c",
                                               client_secret="be6572cfc34e48e6a16c49b1eaf87929",
                                               redirect_uri="http://localhost:3000",
                                               scope="user-library-read user-top-read"))


    def get_most_tracked_artists(self):
        """returns most listened to artists in a time frame using spotipy"""
        results = self.sp.current_user_top_artists(limit=10,
                                                   time_range=TIMEFRAME)
        return results['items']

    def get_most_tracked_songs(self):
        """returns most listened to songs in a time frame using spotipy"""
        results = self.sp.current_user_top_tracks(limit=10,
                                                  time_range=TIMEFRAME)
        return results['items']

    def build(self):
        # Set dark mode background color
        # self.show_template()
        Window.clearcolor = (0.1, 0.1, 0.1, 1)

        layout = BoxLayout(orientation='vertical',
                           spacing=10,
                           padding=10)

        self.time_label = Label(text='Currently tracking the past 6 months!',
                                color=(0.8, 0.8, 0.8, 1),
                                font_size='16sp')
        layout.add_widget(self.time_label)

        self.result_label = Label(text='',
                                  color=(0.8, 0.8, 0.8, 1),
                                  font_size='14sp')
        layout.add_widget(self.result_label)

        button_layout = BoxLayout(orientation='horizontal',
                                  spacing=10,
                                  size_hint=(1, 0.1))

        most_tracked_artists_button = Button(text='Most Tracked Artists',
                                             background_color=(
                                                 0.2, 0.6, 0.9, 1),
                                             font_size='14sp')
        most_tracked_songs_button = Button(text='Most Tracked Songs',
                                           background_color=(0.2, 0.6, 0.9, 1),
                                           font_size='14sp')
        twitter_share_button = Button(text="Tweet",
                                      background_color=(0.2, 0.6, 0.9, 1),
                                      font_size='14sp')
        most_tracked_artists_button.bind(
            on_press=self.show_most_tracked_artists)
        most_tracked_songs_button.bind(
            on_press=self.show_most_tracked_songs)
        twitter_share_button.bind(on_press=self.share_results_twitter)

        button_layout.add_widget(most_tracked_artists_button)
        button_layout.add_widget(most_tracked_songs_button)
        button_layout.add_widget(twitter_share_button)

        layout.add_widget(button_layout)

        time_layout = BoxLayout(orientation='horizontal',
                                spacing=10,
                                size_hint=(1, 0.1))

        time1 = Button(text='Short Term',
                       background_color=(0.2, 0.6, 0.9, 1),
                       font_size='14sp')
        time2 = Button(text='Medium Term',
                       background_color=(0.2, 0.6, 0.9, 1),
                       font_size='14sp')

        time1.bind(on_press=self.short_time)
        time2.bind(on_press=self.med_time)

        time_layout.add_widget(time1)
        time_layout.add_widget(time2)

        layout.add_widget(time_layout)

        return layout

    def short_time(self, instance):
        """changes tracking time frame to approx. past 4 weeks"""
        global TIMEFRAME
        TIMEFRAME = 'short_term'
        self.time_label.text = 'Currently tracking the past 4 weeks!'

    def med_time(self, instance):
        """changes tracking time frame to approx. past 6 months"""
        global TIMEFRAME
        TIMEFRAME = 'medium_term'
        self.time_label.text = 'Currently tracking the past 6 months!'

    def show_most_tracked_artists(self, instance):
        """displays most listened to artists"""
        artists = self.get_most_tracked_artists()
        self.show_results(artists, 0)

    def show_most_tracked_songs(self, instance):
        """displays most listened to songs"""
        songs = self.get_most_tracked_songs()
        self.show_results(songs, 1)

    def share_results_twitter(self, instance):
        """shares app results to the website formerly known as twitter"""
        tweet_text = "Check out the music I listen to:"
        tweet_url = f"https://twitter.com/intent/tweet?text={urllib.parse.quote(tweet_text)}"
        webbrowser.open(tweet_url)

    # def show_template(self):
    #    cover_template = ImageClip(r"/Users/adamjirari/Desktop/SPOTIFY SWE/Black_BG.png").set_duration(5)
    #    cover_template.preview()
    #    topSongs = self.get_most_tracked_songs()
    #    text_labels = {}

    #    for song in topSongs:
    #        label = TextClip(song, fontsize=30, color = "Yellow").set_duration(5)

    # def show_template(self):
    #    cover_template = ImageClip(r"/Users/adamjirari/Desktop/SPOTIFY SWE/Black_BG.png").set_duration(5)
    #    topSongs = self.get_most_tracked_songs()
    #    text_labels = list()

    #    print("Hello")
    #    print(topSongs)
    #    print("Hello")

    #    songCounter = 0
    #    columnCounter = 1
    #    xAxis = 150
    #    yAxis = 1070

    #    for song in topSongs:
    #        songCounter += 1
    #        result_text = f"{song['name']} \n"

    #        label = TextClip(result_text,
    #                         fontsize=30,
    #                         color = "white",
    #                         font = "Arial").set_duration(5)
    #        label = label.set_position((xAxis, yAxis))
    #        yAxis += 68
    #        if songCounter == 5:
    #            xAxis += 450
    #            yAxis = 1070
    #        text_labels.append(label)

    #    for labels in text_labels:
    #        finalTemp = CompositeVideoClip([cover_template, labels])
    #        cover_template = finalTemp

    #    cover_template.write_videofile("output_video.mp4", fps=24)
    # 1 denotes a set of songs, 0 denotes a set of albums (for formatting purposes)
    def show_results(self, items, i):
        """displays formatted results from spotipy requests"""
        result_text = ""
        for item in items:
            if i == 1:
                result_text += f"{item['name']} - {item['artists'][0]['name']}\n"
            else:
                result_text += f"{item['name']}\n"
        self.result_label.text = result_text


#if __name__ == "__main__":
#    SpotifyWrapperApp().run()
