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

    def detect_front_hit_frame(self,f,x,y,NET_LINE,THRESH):
        y_front_index=np.array(y>NET_LINE)
        y_diff=np.diff(y)
        y_diff_index=np.array(abs(y_diff)<THRESH)

        index =y_front_index[:-1] & y_diff_index
        temp=index.astype(np.int)
        i_renzoku=[]
        print(temp)
        for i in range(len(temp)-3):
            if((temp[i]*temp[i+1]*temp[i+2]>0)and (temp[i+3]==0)):
                i_renzoku.append(1)
            else:
                i_renzoku.append(0)
        i_renzoku=np.array(i_renzoku)
        f_shift=f[3:]
        front_hit_array=f_shift[:-1][i_renzoku>0]
        print(front_hit_array)

        x_front_hit_array=[]
        y_front_hit_array=[]
        for i in range(len(front_hit_array)):
            x_front_hit_array.append(x[f==front_hit_array[i]][0])
            y_front_hit_array.append(y[f==front_hit_array[i]][0])
        return x_front_hit_array,y_front_hit_array

    def ball_data2df(self,output_filename):

        f = np.array(self.frame_array)
        x = np.array(self.all_track_ball_x)
        y = np.array(self.all_track_ball_y)

        #パラメータ
        NET_LINE=340
        THRESH=10

        y_rear_index=np.array(y<=NET_LINE)

        #手前側コートの打点タイミング
        x_front_hit_array,y_front_hit_array = self.detect_front_hit_frame(f,x,y,NET_LINE,THRESH)

        #手前側コートのボール着地タイミング
        #84 161 244
        #ひとつ前がプラス変化が大きい　その次に変化が小さい
        y_diff=np.diff(y)
        y_diff_up_index=np.array(y_diff>20)
        y_diff_small_index=np.array(abs(y_diff)<THRESH)
        index=y_diff_up_index[:-1] & y_diff_small_index[1:]
        temp=index.astype(np.int)
        index=temp>0
        f_shift=f[:-1]

        front_bounce_array=f_shift[1:][index]
        print(front_bounce_array)

        x_front_bounce_array=[]
        y_front_bounce_array=[]
        for i in range(len(front_bounce_array)):
            x_front_bounce_array.append(x[f==front_bounce_array[i]][0])
            y_front_bounce_array.append(y[f==front_bounce_array[i]][0])


        #奥側コートのボール着地タイミング

        index =y_rear_index[:-1] & y_diff_index
        temp=index.astype(np.int)

        i_renzoku=[]
        for i in range(len(temp)-3):
            if((temp[i]*temp[i+1]*temp[i+2]>0)and (temp[i+3]==0)):
                i_renzoku.append(1)
            else:
                i_renzoku.append(0)
        i_renzoku=np.array(i_renzoku)
        f_shift=f[3:]

        back_bounce_array=f_shift[:-1][i_renzoku>0]
        print(back_bounce_array)

        x_back_bounce_array=[]
        y_back_bounce_array=[]
        for i in range(len(back_bounce_array)):
            x_back_bounce_array.append(x[f==back_bounce_array[i]][0])
            y_back_bounce_array.append(y[f==back_bounce_array[i]][0])


        #奥側側コートの打点着地タイミング
        #ボール着地タイミングからフレームが30以内の最小値
        range_start=back_bounce_array
        range_end=back_bounce_array+30
        index_min_array=[]
        for i in range(len(range_start)):
            index_range=np.where((f>=range_start[i]) & (f<=range_end[i]))
            index_min=np.argmin(np.array(y[index_range]))
            index_min_array.append(f[f>=range_start[i]][index_min])
        back_hit_array=index_min_array
        print(back_hit_array)

        x_back_hit_array=[]
        y_back_hit_array=[]
        for i in range(len(back_hit_array)):
            x_back_hit_array.append(x[f==back_hit_array[i]][0])
            y_back_hit_array.append(y[f==back_hit_array[i]][0])
            
            

        labels=["Frame","HitBounce"]

        label_front_hit=["Front_Hit"]*len(front_hit_array)
        df1=pd.DataFrame({"Frame":front_hit_array,"HitBounce":label_front_hit,"X_Ball":x_front_hit_array,"Y_Ball":y_front_hit_array})

        label_front_bounce=["Front_Bounce"]*len(front_bounce_array)
        df2=pd.DataFrame({"Frame":front_bounce_array,"HitBounce":label_front_bounce,"X_Ball":x_front_bounce_array,"Y_Ball":y_front_bounce_array})

        label_back_hit=["Back_Hit"]*len(back_hit_array)
        df3=pd.DataFrame({"Frame":back_hit_array,"HitBounce":label_back_hit,"X_Ball":x_back_bounce_array,"Y_Ball":y_back_bounce_array})

        label_back_bounce=["Back_Bounce"]*len(back_bounce_array)
        df4=pd.DataFrame({"Frame":back_bounce_array,"HitBounce":label_back_bounce,"X_Ball":x_back_hit_array,"Y_Ball":y_back_hit_array})

        df=pd.concat([df1,df2,df3,df4])
        df.sort_values('Frame', inplace=True)
        df=df.reset_index()
        df.to_csv(output_filename)


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

if __name__ == "__main__":
    td=TrackData()
    td.load_ball_data("../data/ball-pos.csv")
    output_filename="../data/track_frame-test.csv"
    td.ball_data2df(output_filename)

