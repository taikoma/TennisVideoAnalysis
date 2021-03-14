import unittest
# import pandas as pd

import src.track_data as track_data

class TestTrackData(unittest.TestCase):
    def setUp(self):
        print("setup")
        self.track_data=track_data.TrackData()

    def test_load_ball_data(self):
        filename="./data/ball-pos.csv"
        self.track_data.load_ball_data(filename)
        self.assertEqual([5,819,448],[self.track_data.frame_array[0],self.track_data.all_track_ball_x[0],self.track_data.all_track_ball_y[0]])

    def test_load_track_data(self):
        filename="./data/track-data.csv"
        self.track_data.load_track_data(filename)
        self.assertEqual(1.46,self.track_data.track_ball_x[0])