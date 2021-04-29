import cv2
import math
import numpy as np
import pandas as pd

import score
import database


class SceneDivide():
    def __init__(self):
        pass
    def get_mean_image_bgr(self,filename):#
        """
        画像フレームのBGR平均値を算出し、フレーム毎に配列に格納する
        """
        cap=cv2.VideoCapture(filename)
        b_array=[]
        g_array=[]
        r_array=[]
        count=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        print("count:",count)
        # while True:
        for i in range(0,count):#1000
            print(i)
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret,frame=cap.read()

            if not ret:
                break
                
            b=frame[:,:,0].flatten().mean()
            g=frame[:,:,1].flatten().mean()
            r=frame[:,:,2].flatten().mean()

            b = math.floor(b)#小数点以下を切り捨て
            g = math.floor(g)  
            r = math.floor(r)

            b_array.append(b)
            g_array.append(g)
            r_array.append(r)
            
            # ESCを押したら中止
            k = cv2.waitKey(1) & 0xff
            if k == 27 : break

        print("end")
        return b_array,g_array,r_array

    def calc(self,b_array,g_array,r_array,frame):
        b=b_array[frame]
        g=g_array[frame]
        r=r_array[frame]

        print("BGR",b,g,r)#court 134 109 72,up 107 92 85

        b_per=[]
        g_per=[]
        r_per=[]

        for i in range(0,len(b_array)):
            b_per.append(b_array[i]/b)
            g_per.append(g_array[i]/g)
            r_per.append(r_array[i]/r)
            

        b_per_np=np.array(b_per)
        g_per_np=np.array(g_per)
        r_per_np=np.array(r_per)

        return b_per_np,g_per_np,r_per_np

    def detect_start(self,b_per_np,g_per_np,r_per_np):
        """
        画像の色情報配列から変化率が一定以上のフレームを抽出する
        """
        game_index=np.where((b_per_np>0.9)&(b_per_np<1.1)&(g_per_np>0.9)&(g_per_np<1.1)&(r_per_np>0.9)&(r_per_np<1.1))[0]#コート画像に対して所定以上の色情報差があるフレームを検出
        print("game_index",game_index)
        delta=game_index[1:]-game_index[:-1]#
        # print("delta",delta)

        dist=(delta>1)
        end=game_index[np.where(dist)[0]]
        temp=game_index[1:]
        start=temp[np.where(dist)[0]]

        print(len(start))
        print(start[0])
        print(end[-1])
        if len(start)>0:
            if start[0]>0:
                # start.insert(0,0)
                start=np.insert(start,0,game_index[0])
        if len(end)>0:
            if end[-1]<len(b_per_np)-1:
                # end.insert(-1,len(b_per_np)-1)
                # end=np.insert(end,-1,len(b_per_np)-1)
                end=np.append(end,len(b_per_np)-1)
        return start,end

    def concat_start_end(self):
        #  df_start=pd.read_csv('./start.csv').dropna().astype('int64')
        #  df_end=pd.read_csv('./end.csv').dropna().astype('int64')
         start_np=np.loadtxt('./start.csv')
         end_np=np.loadtxt('./end.csv')
        #  print(start_np)

         df=pd.DataFrame({'StartFrame':start_np,'EndFrame':end_np})
         df.to_csv('./start_end.csv')
    
    def scene_divide(self,video_filename,csv_filename,ref_frame):
        """
        動画ファイルの色情報から、start_frameとend_frameを検出してcsvファイルに保存する
        """
        b_array,g_array,r_array=sd.get_mean_image_bgr(video_filename)

        ref_frame=1413#1418 596
        b_per_np,g_per_np,r_per_np=sd.calc(b_array,g_array,r_array,ref_frame)
        start_frame,end_frame=sd.detect_start(b_per_np,g_per_np,r_per_np)
        print(start_frame)
        print(end_frame)
        np.savetxt('start.csv',start_frame)
        np.savetxt('end.csv',end_frame)
        df=pd.DataFrame({'StartFrame':start_frame,'EndFrame':end_frame})
        df.to_csv(csv_filename)

if __name__ == "__main__":
    sd=SceneDivide()
    video_filename="../video/20210330-nishikori-titipas.avi"
    csv_filename="../data/start_end.csv"
    ref_frame=1413
    sd.scene_divide(video_filename,csv_filename,ref_frame)

    score=score.Score(1)
    db=database.Database('../data/scene-nishikori.db',score)
    db.save_database()

    db.csv2_db_start_end(csv_filename)

