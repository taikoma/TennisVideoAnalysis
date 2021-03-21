import csv
import codecs
import pandas as pd
import numpy as np
import cv2

# from predict import predict as predict
# from predict import playerDetect as playerDetect

class TrackData():
    def __init__(self):
        super().__init__()
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
        self.df2data(df)
    
    def df2data(self,df):
        self.track_frame_array = df["Frame"].astype(np.int64).values.tolist()
        self.track_ball_x = self.df_float2int(df["X_Ball_onC"]).values.tolist()
        self.track_ball_y = self.df_float2int(df["Y_Ball_onC"]).values.tolist()
        self.track_player_a_x = self.df_float2int(df["X_A_onC"]).values.tolist()
        self.track_player_a_y = self.df_float2int(df["Y_A_onC"]).values.tolist()
        self.track_player_b_x = self.df_float2int(df["X_B_onC"]).values.tolist()
        self.track_player_b_y = self.df_float2int(df["Y_B_onC"]).values.tolist()
        self.track_hit_bounce = df["HitBounce"].fillna("").values.tolist()

        self.track_x1 = self.df_float2int(df["X1"]).values.tolist()
        self.track_y1 = self.df_float2int(df["Y1"]).values.tolist()
        self.track_x2 = self.df_float2int(df["X2"]).values.tolist()
        self.track_y2 = self.df_float2int(df["Y2"]).values.tolist()
        self.track_x3 = self.df_float2int(df["X3"]).values.tolist()
        self.track_y3 = self.df_float2int(df["Y3"]).values.tolist()
        self.track_x4 = self.df_float2int(df["X4"]).values.tolist()
        self.track_y4 = self.df_float2int(df["Y4"]).values.tolist()

    def df_float2int(self, df):
        """convert nan to str"" because cannot convert str directly ,once convert to num 999

        Parameters
        ----------
        df:pandas dataframe

        Returns
        ----------
        df:pandas dataframe
        """
        df = pd.to_numeric(df, errors="coerce")
        df = df.fillna(999)
        df = df.astype(np.int64)
        df = df.replace(999, "")
        df = df
        return df

    def df_str2int(self, df):
        """convert nan to str"" because cannot convert str directly ,once convert to num 999

        Parameters
        ----------
        df:pandas dataframe

        Returns
        ----------
        df:pandas dataframe
        """
        df = pd.to_numeric(df, errors="coerce")
        df = df.fillna(999)
        df = df.astype(np.int64)
        df = df.replace(999, "")
        df = df
        return df

    def xy2center(self, x, y):
        """
        convert xy to center reference 
        """
        x = round(x - 10.97/ 2, 2)
        y = round(y - 23.78 / 2, 2)
        return x, y

    def transform_position(self,x,y,matrix):
        """Transform clicked position x,y to tennis court position by using homography matrix

        Parameters
        ----------
        x:float coordinate x in the image
        y:float coorginate y in the image

        Returns
        ----------
        hx:float homography coordinate x
        hy:float homography coordinate y
        """
        pts=np.array([[[float(x),float(y)]]])
        dst = cv2.perspectiveTransform(pts,matrix)#self.M
        hx=round(dst[0][0][0],2)
        hy=round(dst[0][0][1],2)
        hx,hy=self.xy2center(hx,hy)#convert center reference
        return hx,hy

    def predict_court_player(self,track_filename,video_filename):
        # filename="../data/track_frame2.csv"
        with codecs.open(track_filename, "r", "utf-8",errors="ignore") as csv_file:
            df = pd.read_csv(csv_file)

        frame_array=df["Frame"].values.tolist()
        ball_x=df["X_Ball"].values.tolist()
        ball_y=df["Y_Ball"].values.tolist()

        from predict import predict
        filepath="./predict/weights/predict_court_10000.pth"
        predict=predict.Predict(filepath)
        from predict import playerDetect as playerDetect
        filepath="./predict/weights/ssd300_300.pth"
        playerDetect=playerDetect.PlayerDetect(filepath)

        video = cv2.VideoCapture(video_filename)
        frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

        x1_array=[]
        y1_array=[]
        x2_array=[]
        y2_array=[]
        x3_array=[]
        y3_array=[]
        x4_array=[]
        y4_array=[]

        x_ball_court=[]
        y_ball_court=[]

        x_player_a_court=[]
        x_player_b_court=[]
        y_player_a_court=[]
        y_player_b_court=[]

        p1_x_array=[]
        p1_y_array=[]
        p2_x_array=[]
        p2_y_array=[]
        p3_x_array=[]
        p3_y_array=[]
        p4_x_array=[]
        p4_y_array=[]

        for i in range(len(frame_array)):#len(frame_array)
        # for i in range(1):#len(frame_array)
            print(frame_array[i])
            video.set(cv2.CAP_PROP_POS_FRAMES, frame_array[i])
            ok, img = video.read()
            points=predict.predictPoints(img)
            print(points)

            if len(points)>3:
                pts = np.array([points[0],points[1],points[2],points[3]],dtype=int)
                p1=np.array(points[3])
                p2=np.array(points[0])
                p3=np.array(points[1])
                p4=np.array(points[2])
                c1,c2,c3,c4=[10.97, 0],[0, 0],[0, 23.78],[10.97, 23.78]#ダブルスコートの4隅
                src_pts = np.float32([p1,p2,p3,p4]).reshape(-1,1,2)
                dst_pts = np.float32([c1,c2,c3,c4]).reshape(-1,1,2)
                M,mask=cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
                inv_M=np.linalg.inv(M)
                x,y=self.transform_position(ball_x[i],ball_y[i],M)
                print(x,y)

                x1,y1,x2,y2,rx1,ry1,rx2,ry2=playerDetect.detect_player(img)
                xa,ya=self.transform_position(x1,y1,M)
                xb,yb=self.transform_position(x2,y2,M)
                p1_x=p1[0]
                p1_y=p1[1]
                p2_x=p2[0]
                p2_y=p2[1]
                p3_x=p3[0]
                p3_y=p3[1]
                p4_x=p4[0]
                p4_y=p4[1]
                print(xa,ya)
                print(xb,yb)
            else:
                x=""
                y=""
                xa=""
                ya=""
                xb=""
                yb=""
                p1_x=""
                p1_y=""
                p2_x=""
                p2_y=""
                p3_x=""
                p3_y=""
                p4_x=""
                p4_y=""

            x_ball_court.append(x)
            y_ball_court.append(y)    
            x_player_a_court.append(xa)
            y_player_a_court.append(ya)
            x_player_b_court.append(xb)
            y_player_b_court.append(yb)

            p1_x_array.append(p1_x)
            p1_y_array.append(p1_y)
            p2_x_array.append(p2_x)
            p2_y_array.append(p2_y)
            p3_x_array.append(p3_x)
            p3_y_array.append(p3_y)
            p4_x_array.append(p4_x)
            p4_y_array.append(p4_y)

        df["X_Ball_onC"]=x_ball_court
        df["Y_Ball_onC"]=y_ball_court
        df["X_A_onC"]=x_player_a_court
        df["Y_A_onC"]=y_player_a_court 
        df["X_B_onC"]=x_player_b_court
        df["Y_B_onC"]=y_player_b_court

        df["X1"]=p1_x_array
        df["Y1"]=p1_y_array
        df["X2"]=p2_x_array
        df["Y2"]=p2_y_array
        df["X3"]=p3_x_array
        df["Y3"]=p3_y_array
        df["X4"]=p4_x_array
        df["Y4"]=p4_y_array
        df.to_csv("../data/track-data2.csv") 

if __name__ == "__main__":
    td=TrackData()
    # td.load_ball_data("../data/ball-pos-000000-020000.csv")
    # output_filename="../data/track_frame-test.csv"
    # td.ball_data2df(output_filename)
    track_filename="../data/track_frame2.csv"
    video_filename='../video/nishikori-medvedev.avi'
    td.predict_court_player(track_filename,video_filename)

