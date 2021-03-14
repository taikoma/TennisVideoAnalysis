import csv
import codecs
import pandas as pd
import numpy as np

class TrackData():
    def __init__(self):
        print("init")
        self.frame_array=[]
        self.all_track_ball_x=[]
        self.all_track_ball_y=[]

        self.track_frame_array=[]
        self.track_ball_x=[]
        self.track_ball_y=[]
        self.track_player_a_x=[]
        self.track_player_a_y=[]
        self.track_player_b_x=[]
        self.track_player_b_y=[]
        self.track_hit_bounce=[]


    def load_ball_data(self,filename):
        print("load_data")
        
        with codecs.open(filename, "r", "utf-8",errors="ignore") as csv_file:
            df = pd.read_csv(csv_file, header=None)

        labels=["Frame","X","Y"]
        df.columns=labels

        self.frame_array = df["Frame"].astype(np.int64).values.tolist()
        self.all_track_ball_x = df["X"].astype(np.int64).values.tolist()
        self.all_track_ball_y = df["Y"].astype(np.int64).values.tolist()

    def load_track_data(self,filename):
        # print(filename)
        with codecs.open(filename, "r", "utf-8",errors="ignore") as csv_file:
            df = pd.read_csv(csv_file)

        self.track_frame_array = df["Frame"].astype(np.int64).values.tolist()
        self.track_ball_x = df["X_Ball_onC"].astype(np.float).values.tolist()
        self.track_ball_y = df["Y_Ball_onC"].astype(np.float).values.tolist()
        self.track_player_a_x = df["X_A_onC"].astype(np.float).values.tolist()
        self.track_player_a_y = df["Y_A_onC"].astype(np.float).values.tolist()
        self.track_player_b_x = df["X_B_onC"].astype(np.float).values.tolist()
        self.track_player_b_y = df["Y_B_onC"].astype(np.float).values.tolist()
        self.track_hit_bounce = df["HitBounce"].values.tolist()







        
            

