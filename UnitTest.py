import unittest
from unittest.mock import MagicMock, patch

from kivy.tests.common import GraphicUnitTest

import SpotifyWrapperApp


class TestSpotifyWrapperApp(GraphicUnitTest):
    
    def setUp(self):
        super().setUp()
        self.app = SpotifyWrapperApp()
        self.app.build()

    @patch('kivy.core.window.Window.clearcolor') # Mocks the 'clearcolor' attribute of the Kivy Window to simulate changing the background color.
    def test_build_method(self, mock_clearcolor):
        app = SpotifyWrapperApp()
        layout = app.build()

        self.assertIsNotNone(layout)
        self.assertTrue(mock_clearcolor.called)

        # Test the layout hierarchy
        self.assertEqual(len(layout.children), 3)  # Check number of children.
        self.assertEqual(len(layout.children[0].children), 1)  # Check number of time_label's children.
        self.assertEqual(len(layout.children[1].children), 1)  # Check number of result_label's children.
        self.assertEqual(len(layout.children[2].children), 2)  # Check number of button_layout and time_layout's children.

    @patch('spotify_wrapper_app.spotipy.Spotify') # Mock the spotipy.Spotify class.
    def test_get_most_tracked_artists(self, mock_spotify):
        """Test if the 'get_most_tracked_artists' method returns the correct artist using mocked data."""
        mock_spotify.return_value.current_user_top_artists.return_value = {'items': [{'name': 'Artist1'}]}
        app = SpotifyWrapperApp()

        artists = app.get_most_tracked_artists()

        self.assertEqual(len(artists), 1)
        self.assertEqual(artists[0]['name'], 'Artist1')

    @patch('spotify_wrapper_app.spotipy.Spotify')
    def test_get_most_tracked_songs(self, mock_spotify):
        """Test if the 'get_most_tracked_songs' method returns the correct song using mocked data."""
        mock_spotify.return_value.current_user_top_tracks.return_value = {'items': [{'name': 'Song1'}]}
        app = SpotifyWrapperApp()

        songs = app.get_most_tracked_songs()

        self.assertEqual(len(songs), 1)
        self.assertEqual(songs[0]['name'], 'Song1')
        
    def test_short_time_button_click(self):
        """Tests if clicking the 'Short Term' button updates the time label."""
        short_time_button = self.app.root.children[2].children[1].children[0] # Accesses the 'Short Term' button widget located within the app's user interface hierarchy.
        time_label = self.app.root.children[0].children[0] # Retrieves the label widget displaying the tracking time status from the app's user interface structure.
        
        short_time_button.trigger_action(duration=0.1) # Simulates a click action on the 'Short Term' button, updating the tracking time status with a shorter timeframe.
        
        self.assertEqual(time_label.text, 'Currently tracking the past 4 weeks!') # Asserts that after clicking the 'Short Term' button, the time label text is updated correctly.
        
    def test_med_time_button_click(self):
        """Tests if clicking the 'Medium Term' button updates the time label."""
        med_time_button = self.app.root.children[2].children[1].children[1]
        time_label = self.app.root.children[0].children[0]
        
        med_time_button.trigger_action(duration=0.1)
        
        self.assertEqual(time_label.text, 'Currently tracking the past 6 months!')
        
    def test_show_most_tracked_artists(self):
        """Tests if clicking 'Most Tracked Artists' button updates the result label."""
        self.app.get_most_tracked_artists = MagicMock(return_value=[{'name': 'Artist 1'}]) # Mocks the 'get_most_tracked_artists' method of the app to return a predefined list of artists for testing purposes.
        artists_button = self.app.root.children[2].children[0].children[0]
        result_label = self.app.root.children[1].children[0]
        
        artists_button.trigger_action(duration=0.1)
        
        self.assertEqual(result_label.text, 'Artist 1\n')
        
    def test_show_most_tracked_songs(self):
        """Tests if clicking 'Most Tracked Songs' button updates the result label."""
        self.app.get_most_tracked_songs = MagicMock(return_value=[{'name': 'Song 1'}])
        songs_button = self.app.root.children[2].children[0].children[1]
        result_label = self.app.root.children[1].children[0]
        
        songs_button.trigger_action(duration=0.1)
        
        self.assertEqual(result_label.text, 'Song 1\n')
        
if __name__ == '__main__':
    unittest.main()
