from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window


import main

timeframe = 'medium_term'

class SpotifyWrapperApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_most_tracked_artists(self):
        results = main.sp.current_user_top_artists(limit=10,
                                                   time_range=timeframe)
        return results['items']

    def get_most_tracked_songs(self):
        results = main.sp.current_user_top_tracks(limit=10,
                                                  time_range=timeframe)
        return results['items']

    def build(self):
        # Set dark mode background color
        Window.clearcolor = (0.1, 0.1, 0.1, 1)

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        self.time_label = Label(text='Currently tracking the past 6 months!', color=(0.8, 0.8, 0.8, 1), font_size='16sp')
        layout.add_widget(self.time_label)

        self.result_label = Label(text='', color=(0.8, 0.8, 0.8, 1), font_size='14sp')
        layout.add_widget(self.result_label)

        button_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, 0.1))

        most_tracked_artists_button = Button(text='Most Tracked Artists', background_color=(0.2, 0.6, 0.9, 1), font_size='14sp')
        most_tracked_songs_button = Button(text='Most Tracked Songs', background_color=(0.2, 0.6, 0.9, 1), font_size='14sp')

        most_tracked_artists_button.bind(on_press=self.show_most_tracked_artists)
        most_tracked_songs_button.bind(on_press=self.show_most_tracked_songs)

        button_layout.add_widget(most_tracked_artists_button)
        button_layout.add_widget(most_tracked_songs_button)

        layout.add_widget(button_layout)

        time_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, 0.1))

        time1 = Button(text='Short Term', background_color=(0.2, 0.6, 0.9, 1), font_size='14sp')
        time2 = Button(text='Medium Term', background_color=(0.2, 0.6, 0.9, 1), font_size='14sp')

        time1.bind(on_press=self.short_time)
        time2.bind(on_press=self.med_time)

        time_layout.add_widget(time1)
        time_layout.add_widget(time2)

        layout.add_widget(time_layout)

        return layout

    def short_time(self, instance):
        global timeframe
        timeframe = 'short_term'
        self.time_label.text = 'Currently tracking the past 4 weeks!'

    def med_time(self, instance):
        global timeframe
        timeframe = 'medium_term'
        self.time_label.text = 'Currently tracking the past 6 months!'

    def show_most_tracked_artists(self, instance):
        artists = self.get_most_tracked_artists()
        self.show_results(artists, 0)

    def show_most_tracked_songs(self, instance):
        songs = self.get_most_tracked_songs()
        self.show_results(songs, 1)

    # 1 denotes a set of songs, 0 denotes a set of albums (for formatting purposes)
    def show_results(self, items, i):
        result_text = ""
        for item in items:
            if i == 1:
                result_text += f"{item['name']} - {item['artists'][0]['name']}\n"
            else:
                result_text += f"{item['name']}\n"
        self.result_label.text = result_text


if __name__ == "__main__":
    SpotifyWrapperApp().run()
