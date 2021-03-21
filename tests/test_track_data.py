import unittest
# import pandas as pd
import numpy as np
import pandas as pd

import src.track_data as track_data

class TestTrackData(unittest.TestCase):
    def setUp(self):
        print("setup")
        self.track_data=track_data.TrackData()

    def test_load_ball_data(self):
        filename="./data/ball-pos.csv"
        self.track_data.load_ball_data(filename)
        self.assertEqual([5,819,448],[self.track_data.frame_array[0],self.track_data.all_track_ball_x[0],self.track_data.all_track_ball_y[0]])

    def test_df2data(self):
        frame=[100,200,300,400,500]
        x_ball=[np.NaN]*5
        y_ball=[np.NaN]*5
        x_a=[""]*5
        y_a=[""]*5
        x_b=[""]*5
        y_b=[""]*5
        hb=[""]*5
        x1,y1,x2,y2,x3,y3,x4,y4=[""]*5,[""]*5,[""]*5,[""]*5,[""]*5,[""]*5,[""]*5,[""]*5
        df=pd.DataFrame({"Frame":frame,
                            "X_Ball_onC":x_ball,
                            "Y_Ball_onC":y_ball,
                            "X_A_onC":x_a,
                            "Y_A_onC":y_a,
                            "X_B_onC":x_b,
                            "Y_B_onC":y_b,
                            "HitBounce":hb,
                            "X1":x1,
                            "Y1":y1,
                            "X2":x2,
                            "Y2":y2,
                            "X3":x3,
                            "Y3":y3,
                            "X4":x4,
                            "Y4":y4}
                            )
        self.track_data.df2data(df)
        self.assertEqual(len(self.track_data.track_frame_array),len(self.track_data.track_x1))


    @unittest.skip("test")
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