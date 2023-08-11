import unittest
from unittest.mock import MagicMock
from kivy.tests.common import GraphicUnitTest

import SpotifyWrapperApp

class TestSpotifyWrapperApp(GraphicUnitTest):
    
    def setUp(self):
        super().setUp()
        self.app = SpotifyWrapperApp()
        self.app.build()
        
    def test_short_time_button_click(self):
        """Tests if clicking the 'Short Term' button updates the time label"""
        short_time_button = self.app.root.children[2].children[1].children[0]
        time_label = self.app.root.children[0].children[0]
        
        short_time_button.trigger_action(duration=0.1)
        
        self.assertEqual(time_label.text, 'Currently tracking the past 4 weeks!')
        
    def test_med_time_button_click(self):
        """Tests if clicking the 'Medium Term' button updates the time label"""
        med_time_button = self.app.root.children[2].children[1].children[1]
        time_label = self.app.root.children[0].children[0]
        
        med_time_button.trigger_action(duration=0.1)
        
        self.assertEqual(time_label.text, 'Currently tracking the past 6 months!')
        
    def test_show_most_tracked_artists(self):
        """Tests if clicking 'Most Tracked Artists' button updates the result label"""
        self.app.get_most_tracked_artists = MagicMock(return_value=[{'name': 'Artist 1'}])
        artists_button = self.app.root.children[2].children[0].children[0]
        result_label = self.app.root.children[1].children[0]
        
        artists_button.trigger_action(duration=0.1)
        
        self.assertEqual(result_label.text, 'Artist 1\n')
        
    def test_show_most_tracked_songs(self):
        """Tests if clicking 'Most Tracked Songs' button updates the result label"""
        self.app.get_most_tracked_songs = MagicMock(return_value=[{'name': 'Song 1'}])
        songs_button = self.app.root.children[2].children[0].children[1]
        result_label = self.app.root.children[1].children[0]
        
        songs_button.trigger_action(duration=0.1)
        
        self.assertEqual(result_label.text, 'Song 1\n')
        
if __name__ == '__main__':
    unittest.main()
