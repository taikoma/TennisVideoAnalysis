import unittest
# import pandas as pd
import numpy as np

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

    def test_detect_front_hit_frame(self):
        NET_LINE=340
        THRESH=10
        f=np.array([0,10,11,12,13,14,15,20,21,30])
        x=np.array([0,1,2,3,4,5,6,7,8,9])
        y=np.array([300,400,500,595,596,594,590,500,400,300])
        x_array,y_array=self.track_data.detect_front_hit_frame(f,x,y,NET_LINE,THRESH)
        self.assertEqual([6],x_array)
        self.assertEqual([590],y_array)

        f=np.array([])
        x=np.array([])
        y=np.array([])
        x_array,y_array=self.track_data.detect_front_hit_frame(f,x,y,NET_LINE,THRESH)
        self.assertEqual([],x_array)
        self.assertEqual([],y_array)